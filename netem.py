#!/usr/bin/env python
#coding:utf-8

import sys
import os
import re
import Queue
import time
import copy
import multiprocessing
import cPickle as pickle
from keystoneauth1.identity import v3
from keystoneauth1 import session
from neutronclient.v2_0 import client as neutron_client
from novaclient import client as nova_client
import community

BASE_URL='http://192.168.99.112' 
AUTH_URL=BASE_URL + ':35357/v3'
NEUTRON_URL=BASE_URL + ':5000/v2.0'
TOKEN='admin'
USERNAME='admin'
PASSWORD='bjtungirc'
PROJECT_NAME='demo'
PROJECT_ID='11e5aab9a4d246c598e06c807c18383f'
USER_DOMAIN_ID='default'
PROJECT_DOMAIN_ID='default'
EMU_NETWORK='private2'

HOSTS_PATH='/etc/hosts'
MANIFESTS_PATH='/etc/puppet/manifests/site.pp'
IBR_CONFIG='/etc/puppet/files/ibrdtnd.conf'
PICKLE_PATH='/etc/puppet/files/pickle/'

def create_session():
    auth = v3.Password(auth_url=AUTH_URL, username=USERNAME,
                       password=PASSWORD, project_name=PROJECT_NAME,
                       user_domain_id=USER_DOMAIN_ID, project_domain_id=PROJECT_DOMAIN_ID)
    sess = session.Session(auth=auth, )
    return sess

def update_etc_hosts(nova, hosts_path):
    '''update /etc/hosts,add the new experimental nodes,
    if an experimental node existed in hosts file, update it.
    '''

    #hosts_path = '/home/os/hh.txt'
    servers = nova.servers.list()
    with open(hosts_path, 'r') as hosts_obj:
        old_content = hosts_obj.read()

    with open(hosts_path, 'w') as hosts_obj:
        for server in servers:
            name = server.name
            addr = server.addresses['flat'][0]['addr']
            line = addr + ' ' + name
            if re.search(name+r'$', old_content):
                content = re.sub(r'.*'+name+r'$', line, old_content)
            else:
                content = old_content + '\n' + line

            old_content = content
        hosts_obj.write(content)

def get_emu_ports(nova, neutron, network_name):
    '''hosts2ports is dict, key:hostname, value:[id, ip]'''
    servers = nova.servers.list()
    ports_dict = neutron.list_ports()
    ports = ports_dict['ports']
    hosts2ports = {}
    for server in servers:
        emu_host = server.name
        emu_addr = server.addresses[network_name][0]['addr']
        flat_addr = server.addresses['flat'][0]['addr']
        index = 0
        for index in range(len(ports)):
            if flat_addr == ports[index]['fixed_ips'][0]['ip_address']:
                ports.pop(index)
            if len(ports) == 0: break
            if emu_addr == ports[index]['fixed_ips'][0]['ip_address']:
                #ns+ id[:11]
                hosts2ports[emu_host] = [ports[index]['id'],
                               ports[index]['fixed_ips'][0]['ip_address'],] 
                ports.pop(index)
                break
            index = index + 1
    return hosts2ports       
    
def create_security_groups(hosts2ports, neutron):
    new_sec_groups = {}
    sec_groups = neutron.list_security_groups()['security_groups']
    for name, port in hosts2ports.iteritems():
        for sec in sec_groups:
            if sec['tenant_id'] != PROJECT_ID: continue
            if sec['name'] == name:
                #delete
                neutron.delete_security_group(
                              sec['security_group_rules'][0]['security_group_id'])

	 
        #create group
        security_group ={
              'name':name,
              'description':'permit pakcets, whose src ip is ' + name +' emu_addr',
              }
        sec_group = neutron.create_security_group(
                                          {'security_group':security_group})
        sec_group_rules = sec_group['security_group']['security_group_rules']
        sec_group_id = sec_group_rules[0]['security_group_id']
        new_sec_groups[name] = sec_group_id
        #create rules
        sec_rules = [
                    {
                    'direction':'ingress',
                    'remote_ip_prefix': port[1] + '/32',
                    'ethertype':'IPv4',
                    'security_group_id':sec_group_id,
                    },
                    ]
        neutron.create_security_group_rule({'security_group_rules':sec_rules})
    return new_sec_groups

def get_security_groups(hosts, neutron):
    '''group_name => group_i'''
    new_sec_groups = {}
    sec_groups = neutron.list_security_groups()['security_groups']
    for sec_group in sec_groups:
        name = sec_group['name']
        if hosts.count(name) == 1: 
            new_sec_groups[name] = \
                     sec_group['security_group_rules'][0]['security_group_id']
    return new_sec_groups            
    
def compare_list(list1, list2):
    if len(list1) != len(list2): return False
    for i in range(len(list1)):
        if list1[i] != list2[i]: return False
    return True

def _topology_ctl(cgr_old, cgr, hosts2ports, sec_groups, neutron, test=False):
    diff = len(cgr)
    for i in range(len(cgr)):
        new_sec_groups = []
        if len(cgr_old):
            if compare_list(cgr[i], cgr_old[i]): 
                diff = diff - 1
                continue
        
        if test == True: continue
        for j in range(len(cgr[i])):
            if i == j: continue   
            #contacted
            if cgr[i][j] == 1:
                name = 'ibr-' + str(j+1)
                new_sec_groups.append(sec_groups[name])

        name = 'ibr-' + str(i+1)
#        pid = os.fork()
        #child process
 #       if pid == 0:
        neutron.update_port(hosts2ports[name][0],
                                {'port':
                                 {
                                  'security_groups':new_sec_groups,
                                 }
                                })
    return diff

def topology_ctl(cgr_q, hosts2ports, sec_groups, neutron, test=False):
    cgr_old = []
    max_diff = 0
    max_diff_cgr = []
    max_diff_cgr_old = []
    while not cgr_q.empty():   
        cgr = cgr_q.get()
        diff = _topology_ctl(cgr_old, cgr, hosts2ports,sec_groups, neutron, test)
        if max_diff < diff: 
            max_diff = diff
            max_diff_cgr = cgr 
            max_diff_cgr_old = cgr_old 
        
        #test to obtain time_unit, the long time to change once topology
        if cgr_q.empty() and test:
            start = time.time()
            _topology_ctl(max_diff_cgr_old, max_diff_cgr,
                          hosts2ports,sec_groups, neutron, False)
            end =  time.time()
            print "%.5f" % (end-start)
            yield "%.5f" % (end-start)
            break
            
        cgr_old = cgr 
        yield True

def common_config(file_obj):
    config_str = '''
class ibrdtn_config {
    file { "/etc/ibrdtn/ibrdtnd.conf":
        ensure => present,
        mode => 666,
        owner => root,
        group => root,
        source =>"puppet://os/files/ibrdtnd.conf"
    }
}

class time_execute {
    file { "/usr/bin/te":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/te"
    }
}

class killdtn_file {
    file { "/usr/bin/killdtn":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/killdtn"
    }
}

class killagent_file {
    file { "/usr/bin/killagent":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/killagent"
    }
}

class netem-agent_file {
    file { "/usr/bin/netem-agent":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/netem-agent"
    }
}
class time_iptables{
    file {"/usr/bin/test_time":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/test_time"
    }

}

class test_time{
    exec {"test_time":
        path => "/usr/bin/:/usr/sbin/:/usr/local/bin:/usr/local/sbin:/sbin/:/bin"
    }
}

class killdtn{
    exec {"killdtn":
        path => "/usr/bin/:/usr/sbin/:/usr/local/bin:/usr/local/sbin:/sbin/:/bin"
    }
}

class killagent{
    exec {"killagent":
        path => "/usr/bin/:/usr/sbin/:/usr/local/bin:/usr/local/sbin:/sbin/:/bin"
    }
}

class pre_command {
    exec {"mount -t nfs 192.168.99.112:/home/exp /root/exp":
           path => "/usr/bin/:/usr/sbin/:/usr/local/bin:/usr/local/sbin:/sbin/:/bin"
    }
}
''' 
    file_obj.write(config_str)

def pickle_pp(path_dir, host_index):
    common_str = '''
    file { "/tmp/%s":
        ensure => present,
        mode => 777,
        owner => root,
        group => root,
        source =>"puppet://os/files/pickle/%s"
    }

'''
    cgr_str = ''
    senders_str = ''
    receivers_str = ''
    name = 'hosts2ports'
    if os.path.exists(path_dir + name):
        hosts2ports_str = common_str % (name, name)
   
    name = 'cgr_l.' + str(host_index + 1)
    if os.path.exists(path_dir + name):
        cgr_str = common_str % (name, name)
   
    name = 'senders.' + str(host_index + 1)
    if os.path.exists(path_dir + name):
        senders_str = common_str % (name, name)

    name = 'receivers.' + str(host_index + 1)
    if os.path.exists(path_dir + name):
        receivers_str = common_str % (name, name)

    pickle_str = hosts2ports_str + cgr_str + senders_str + receivers_str 
    return pickle_str
    

def create_node_rec_command(dst_host, src_hosts):
    '''dst_host is list index, start from 0,
       dst_host is the host receiving dtn
       src_hosts is list as [[src_index,0],.....]
       dtnrecv --name src_dst_NUM --file /root/exp/ibr/rec/src_dst_NUM.txt
    '''
    send_count = {}
    dst_name = 'ibr-' + str(dst_host + 1)
    command = ""
    for src in src_hosts:
        src_index = src[0]
        src_name = 'ibr-' + str(src_index + 1)
        if not send_count.has_key(src_name):
            send_count[src_name] = 1
        src_dst_num = src_name + "_" + dst_name +\
                  "_" + str(send_count[src_name])
        command = command + 'dtnrecv --name ' + src_dst_num +\
               " --file /root/exp/ibr/rec/" + src_dst_num + ".txt & " 
        send_count[src_name] = send_count[src_name] + 1
    return command


def create_file(file_path, content, size):
    '''size unit is Bytes'''
    content = content + '\n'
    left_content = ''
    cnt = size/len(content)
    if size%len(content): left_content = '1'*(size%len(content))
    with open(file_path, 'w') as file_obj:
        for i in range(cnt):
            file_obj.write(content)
        if left_content: file_obj.write(left_content)
    
def create_node_send_command(src_host, dst_hosts, time_unit, time_after):
    '''src_host is list index, start from 0,
       src_host is the host sending dtn
       dst_hosts is list [[host_index, time_index], [],...]
       te timestamp "dtnsend dtn://dst/src_dst_NUM /root/exp/ibr/send/src_dst_NUM.txt"
    '''
    send_count = {}
    src_name = 'ibr-' + str(src_host + 1)
    command = ""
    pre_time = time.time() + time_after
    for dst in dst_hosts:
        dst_index = dst[0]
        time_index = dst[1]
        dst_name = 'ibr-' + str(dst_index + 1)
        if not send_count.has_key(dst_name):
            send_count[dst_name] = 1
        src_dst_num = src_name + "_" + dst_name +\
                      "_" + str(send_count[dst_name])
        file_path = '/root/exp/ibr/send/' + src_dst_num + '.txt'
        create_file(file_path, src_dst_num, 1024)
              
        exc_time = int(time_index*time_unit + pre_time)
        command = command + 'te ' + str(exc_time) + ' "' +\
                  'dtnsend dtn://' + dst_name + '/' + src_dst_num + ' ' +\
                  file_path + '" & '
        send_count[dst_name] = send_count[dst_name] + 1
        
    return command
        
def create_manifests(senders, receivers,hosts2ports, time_unit, time_after):
    '''creat puppet manifest, basing on mobility model,
    '''
    last_host_num = max(senders.keys() +  receivers.keys())
    with open(MANIFESTS_PATH, 'w') as file_obj:
        common_config(file_obj)
#    sys.exit(0)
        for i in range(last_host_num + 1):
            name = 'ibr-' + str(i+1)
            port_id = hosts2ports[name][0]
            interface =  'ns' + port_id[:11]
            onlyif = "dtnd -c /etc/ibrdtn/ibrdtnd.conf -i " +\
                       interface + " &"
            command = "ifstat -i " + interface +\
                       " >/root/exp/ibr/net/" + name + ".txt & "
            if receivers.has_key(i):
                cmd = create_node_rec_command(i, receivers[i]) 
                command = command + cmd
            if senders.has_key(i): 
                cmd = create_node_send_command(i, senders[i], time_unit, time_after)
                command = command + cmd
            #     '\tinclude pre_command\n' +\
            str_config = 'node "' + name + '"{\n' + \
                 '\tinclude ibrdtn_config\n' + \
                 '\tinclude time_execute\n' +\
                 '\tinclude pre_command\n' +\
                 '\tinclude time_iptables\n' +\
                 '\tinclude netem-agent_file\n' +\
                 '\tinclude killdtn_file\n'
            if  time_after > 0:
                str_config = str_config + \
                     '\texec {\'' + command +'\':\n' +\
                     '\t\tpath => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",\n' + \
                     '\t\tonlyif => "' + onlyif +  '"\n\t}\n}\n\n'
            elif time_after < 0:
                #str_config = str_config + '\tinclude killdtn\n}\n\n'
                str_config = str_config + '\tinclude test_time\n}\n\n'
            elif time_after == 0:
                str_config = str_config + '}\n\n'
            file_obj.write(str_config)

def create_manifests2(host_num, hosts2ports, time_after, time_unit):
    '''creat puppet manifest, basing on mobility model,
    '''
    exec_time = time.time() + time_after
    print "exec_time:%s, time_unit:%s" % (str(exec_time), str(time_unit))
    with open(MANIFESTS_PATH, 'w') as file_obj:
        common_config(file_obj)
#    sys.exit(0)
        for i in range(host_num):
            pickle_str = pickle_pp(PICKLE_PATH, i)
            name = 'ibr-' + str(i+1)
            port_id = hosts2ports[name][0]
            interface =  'ns' + port_id[:11]
           # onlyif = "dtnd -c /etc/ibrdtn/ibrdtnd.conf -i " +\
           #            interface + " &"
            command = "ifstat -i " + interface +\
                       " >/root/exp/ibr/net/" + name + ".txt & " +\
                      "netem-agent " + str(exec_time) + " 500 " + str(time_unit) + " & "
                      #"netem-agent " + str(exec_time) + " 5 " + str(time_unit) + " &"
            #     '\tinclude pre_command\n' +\
            str_config = 'node "' + name + '"{\n' + \
                 '\tinclude ibrdtn_config\n' + \
                 '\tinclude time_execute\n' +\
                 '\tinclude pre_command\n' +\
                 '\tinclude time_iptables\n' +\
                 '\tinclude netem-agent_file\n' +\
                 '\tinclude killagent_file\n' +\
                 '\tinclude killdtn_file\n' 
            if  time_after > 0:
                str_config = str_config + pickle_str +\
                     '\texec {\'' + command +'\':\n' +\
                     '\t\tpath => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",\n' + \
                     '\t}\n}\n\n'
            elif time_after < 0:
                str_config = str_config + '\tinclude killagent\n'
                str_config = str_config + '\tinclude killdtn\n}\n\n'
                #str_config = str_config + '\tinclude test_time\n}\n\n'
            elif time_after == 0:
                str_config = str_config + pickle_str +'}\n\n'
            file_obj.write(str_config)

def put_list(cgr_l, cgr):
    for i, cgr_s in enumerate(cgr):
        if len(cgr_l) <= i:
            cgr_l[i] = []
            cgr_l[i].append(cgr_s)
        else:
            cgr_l[i].append(cgr_s)

def cgr_iptables_num(cgr_old, cgr):
    '''return the times of a host calling cmd iptables(insert/delete),
       from cgr_old state to cgr state
       cgr [0, 1, 0,...]
    '''
    count = 0
    if len(cgr_old) != len(cgr): return cgr.count(1)
    for i,elem in  enumerate(cgr):
        if elem + cgr_old[i] == 1:
                count = count + 1
    return count

def max_iptables_num(cgr_l):
    max_num = 0
    for cgr in cgr_l.itervalues():
        cgr_s_old  = []
        for cgr_s in cgr:
            num = cgr_iptables_num(cgr_s_old, cgr_s)
            if num > max_num: max_num = num
            cgr_s_old = cgr_s
    return max_num

def pickle_dump(coordiantes_l, cgr_l, hosts2ports, senders, receivers):
    if not os.path.isdir(PICKLE_PATH): os.makedirs(PICKLE_PATH)
    path = PICKLE_PATH + 'coordiantes_l'
    with open(path, 'wb') as f:
        pickle.dump(coordiantes_l, f)

    path = PICKLE_PATH + 'hosts2ports'
    with open(path, 'wb') as f:
        pickle.dump(hosts2ports, f)

    path = os.path.join(PICKLE_PATH, 'cgr_l')
    with open(path, 'wb') as f:
        pickle.dump(cgr_l, f)

    path = os.path.join(PICKLE_PATH, 'senders')
    with open(path, 'wb') as f:
        pickle.dump(senders, f)

    path = os.path.join(PICKLE_PATH, 'receivers')
    with open(path, 'wb') as f:
        pickle.dump(receivers, f)

    for i, cgr in cgr_l.iteritems():
        path = PICKLE_PATH + 'cgr_l' + '.' + str(i + 1)
        with open(path, 'wb') as f:
            pickle.dump(cgr, f)

        if senders.has_key(i):
            path = PICKLE_PATH + 'senders' + '.' + str(i + 1)
            with open(path, 'wb') as f:
                pickle.dump(senders[i], f)
          
        if receivers.has_key(i):
            path = PICKLE_PATH + 'receivers' + '.' + str(i + 1)
            with open(path, 'wb') as f:
                pickle.dump(receivers[i], f)


def main():
    try:
        time_after = int(sys.argv[1])
        first_flag = sys.argv[2]
        run_model_flag = sys.argv[3]
    except:
        help_info = "Usage:%s <time_after> <first_flag>(True/False) <run_model_flag> [t_count]\n" % sys.argv[0]
        help_info = help_info + "\t <time_after> after these seconds,start emulation\n"
        help_info = help_info + "\t time_after == 0, generate trasfering file puppet file\n"
        help_info = help_info + "\t time_after < 0, generate killdtn puppet file\n"
        help_info = help_info + "\t time_after > 0, generte doing some experiments puppet file\n"
        help_info = help_info + "\t <first_flag> True: generate hosts, False: do not\n"
        help_info = help_info + "\t <run_model_flag> True: run model, False:use generated model data\n"
        help_info = help_info + "\t [t_count] is empty, Do  experiments to the end\n"
        help_info = help_info + "\t t_count > 0, after t_count time, break experiments\n"
	print help_info
        sys.exit(-1)

    t_count = 0
    try: 
       t_count = sys.argv[4]
    except:
        pass

    if run_model_flag == 'True':
        run_model_flag = True
    else:
        run_model_flag = False

    sess = create_session()
    nova = nova_client.Client('2', session=sess, )
    neutron = neutron_client.Client(auth_url=NEUTRON_URL, tenant_name=PROJECT_NAME,
                                               username=USERNAME,password=PASSWORD)
    hosts2ports = get_emu_ports(nova, neutron, EMU_NETWORK)
    if first_flag == 'True':
        update_etc_hosts(nova, HOSTS_PATH)

    cgr_l = {}
    model = community.Model()
    model_iter = model.run()
    time_count = 0
    time_unit = 1
    sender_count = 0
    senders = {}
    receivers = {}
    coordiantes_l = []
    #generate emulation data and file
    while model_iter and time_after > 0 and run_model_flag:
        try:
            #cgr:[[],[],...], sender:[src_index, dst_index](0, 1,...)
            cgr, sender = model_iter.next()
        except StopIteration:
            break
     
        coordiantes = copy.deepcopy(model.coordiantes)
        coordiantes_l.append(coordiantes)
        put_list(cgr_l, cgr)
        if len(sender):
            sender_count = sender_count + 1
            if not senders.has_key(sender[0]): senders[sender[0]] = []
            senders[sender[0]].append([sender[1], time_count])
           
            if not receivers.has_key(sender[1]): receivers[sender[1]] = []
            receivers[sender[1]].append([sender[0], 0])
        time_count = time_count + 1
        if t_count > 0  and  time_count > t_count: break

    #print max_iptables_num(cgr_l)
    #sys.exit(0)
    if time_after > 0 and run_model_flag:
        pickle_dump(coordiantes_l, cgr_l, hosts2ports, senders, receivers)
    create_manifests2(len(hosts2ports), hosts2ports, time_after, 1)

if __name__ == "__main__":
    sys.exit(main())
