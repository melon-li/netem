#!/usr/bin/env python
#coding:utf-8

import sys
import os
import re
import Queue
import time
import copy
import multiprocessing
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

def topology_ctl(cgr_q, hosts2ports, sec_groups, neutron):
    cgr_old = []
    while not cgr_q.empty():   
        cgr = cgr_q.get()
        for i in range(len(cgr)):
            new_sec_groups = []
            if len(cgr_old):
                if compare_list(cgr[i], cgr_old[i]): continue
            for j in range(len(cgr[i])):
                if i == j: continue   
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
                 ''' 
    file_obj.write(config_str)

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
               " --file /root/exp/ibr/rec/" + src_dst_num + ".txt & >/dev/null;" 
        send_count[src_name] = send_count[src_name] + 1

def create_node_send_command(time_unit, time_after, src_host, dst_hosts):
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
        if not send_count.has_key(src_name):
            send_count[dst_name] = 1
        src_dst_num = src_name + "_" + dst_name +\
            "_" + str(send_count[dst_name])
        exc_time = time_index*time_unit + pre_time 
        command = command + 'te ' + str(exc_time) + ' "' +\
                  'dtnsend dtn://' + dst_name + '/' + str_dst_num +\
                  '/root/exp/ibr/send/' + src_dst_num + '.txt' + '"'
        send_count[src_name] = send_count[src_name] + 1
        
        
def create_manifests(senders, receivers, time_unit, after_time):
    '''creat puppet manifest, basing on mobility model,
       te timestamp "dtnsend dtn://dst/src-NUM /root/exp/ibr/send/src-dst-NUM.txt"
       dtnrecv --name src-NUM --file /root/exp/ibr/rec/src-dst-NUM.txt
    '''
    pre_time = time.time() + after_time
    last_host_num = max(senders.keys() +  receivers.keys())
    with open(MANIFESTS_PATH, 'w') as file_obj:
        common_config(file_obj)
    sys.exit(0)
        for i in range(last_host_num + 1):
            if receivers.has_key(i):
                exc_time = pre_time
                command = "dtnd -i /etc/ibrdtn/ibrdtnd.conf;"
                for src in receivers[i]:
                    src_num = 'ibr-' + str(src+1) + "-"
                    command = command + "dtnrecv --name " +  
            if 
            name = 'ibr-' + str(i)
            exc_time = 
            command = "te " + pre_time
        
    pass


def main():
    try:
        after_time = int(sys.argv[1])
        first_flag = sys.argv[2]
    except:
        print "Usage:%s start_time first_flag(True/False)\n\tafter start_time second,start emulation" % sys.argv[0]
        sys.exit(-1)

    create_manifests({},{},0,0)
    sys.exit(0)
    sess = create_session()
    nova = nova_client.Client('2', session=sess, )
    neutron = neutron_client.Client(auth_url=NEUTRON_URL, tenant_name=PROJECT_NAME,
                                               username=USERNAME,password=PASSWORD)
    hosts2ports = get_emu_ports(nova, neutron, EMU_NETWORK)
    if first_flag == 'True':
        sec_groups = create_security_groups(hosts2ports, neutron)
        update_etc_hosts(nova, HOSTS_PATH)
    else:
        sec_groups = get_security_groups(hosts2ports.keys(), neutron)

    #from pprint import pprint
    #pprint(sec_groups)
    #sys.exit(0)
    cgr_q = Queue.Queue(0)
    model = community.Model()
    model_iter = model.run()
    time_count = 0
    time_unit = 1
    sender_count = 0
    senders = {}
    receivers = {}
    while model_iter:
        try:
            #cgr:[[],[],...], sender:[src_index, dst_index](0, 1,...)
            cgr, sender = model_iter.next()
        except StopIteration:
            break
        cgr_q.put(cgr)
        if len(sender):
            sender_count = sender_count + 1
            if not senders.has_key(sender[0]): senders[sender[0]] = []
            senders[sender[0]].append([sender[1], time_count])
           
            if not receivers.has_key(sender[1]): receivers[sender[1]] = []
            receivers[sender[1]].append([sender[0], 0])
        time_count = time_count + 1


    topology_ctl_iter = topology_ctl(cgr_q, hosts2ports, sec_groups, neutron)
    time_seq = []
    for i in range(600):
        start = time.time()
        topology_ctl_iter.next()
        end = time.time()
        time_seq.append(end-start)
        time.sleep(0.01)
        
    for v in time_seq:
        print "time:%.5f" % (v, )
    
    #for k,v in senders.iteritems():
    #   print "node %d: send num %d" % (k,len(v))
    #print "send_count :%d" % sender_count
    #print ""
    #print "time_count:%s" % time_count
    #print ""
    #sum = 0
    #while not cgr_q.empty(): 
    #    cgr = cgr_q.get()
    #    sum = sum + cgr[55].count(1)
    #print("sum:",sum )
if __name__ == "__main__":
    sys.exit(main())
