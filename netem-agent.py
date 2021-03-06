#!/usr/bin/python
#coding:utf-8
import os
import sys
import time
import cPickle as pickle

BASE_PATH = "/root/exp/ibr/"

def get_host_num(path):
    files = os.listdir(path)
    for name in files:
        if name.find('cgr_l') >= 0: 
            pos = name.find('.') + 1
            return int(name[pos:])
    return -1

def log_error(host_num, error_str):
    dir_path = BASE_PATH + "log"
    if not os.path.isdir(dir_path): os.makedirs(dir_path)
    name = 'log_error.' + 'ibr-' + str(host_num)
    file_path = os.path.join(dir_path, name)
    with open(file_path, 'w+') as f:
        f.write(error_str + '\n')
        
def rm_logdir():
    dir_path = BASE_PATH + "log"
    if os.path.isdir(dir_path):
        cmd = 'rm -rf ' + dir_path
        os.system(cmd)       

def init(host_num, hosts2ports):
    name = 'ibr-' + str(host_num)
    port_id = hosts2ports[name][0]
    interface =  'ns' + port_id[:11]
    cmd = '/sbin/iptables -F & '
    cmd = cmd + "/sbin/iptables -I INPUT -i %s -j DROP &"

    rm_logdir()
    if os.system(cmd % (interface,)):
        error_str = 'Failed: ' + start_cmd
        log_error(host_num, error_str)
        sys.exit(-1)


        
def compare_cgr(cgr_old, cgr):
    '''1: add the iptables item,host index is the seq
       0: not change
       -1: delete the ipatables item
    '''
    cgr_c = []
    if len(cgr_old) != len(cgr): return cgr
    for i,elem in  enumerate(cgr):
        if elem == 0:
            if cgr_old[i] == 1:
                cgr_c.append(-1)
            else:
                cgr_c.append(0)
        elif elem == 1:
            if cgr_old[i] == 1:
                cgr_c.append(0)
            else:
                cgr_c.append(1)
    return cgr_c

def topology_ctl(host_num, cgr_l, hosts2ports, test=False):
    cgr_old = []
    name = 'ibr-' + str(host_num)
    port_id = hosts2ports[name][0]
    interface =  'ns' + port_id[:11]
    for cgr in cgr_l:
        cgr_c = compare_cgr(cgr_old, cgr)
        for index, state in enumerate(cgr_c):
            name = 'ibr-' + str(index + 1)
            src_ip = hosts2ports[name][1]
            if state == -1:
                command = '/sbin/iptables -D INPUT -i %s -p ip --src %s -j ACCEPT'
                command = command % (interface, src_ip)
                os.system(command)
            elif state == 1:
                command = '/sbin/iptables -I INPUT -i %s -p ip --src %s -j ACCEPT'
                command = command % (interface, src_ip)
                os.system(command)
  
        cgr_old = cgr
        yield True

def create_node_rec_command(dst_host, src_hosts):
    '''dst_host is list index, start from 0,
       dst_host is the host receiving dtn
       src_hosts is list as [[src_index,0],.....]
       dtnrecv --name src_dst_NUM --file /root/exp/ibr/rec/src_dst_NUM.txt
    '''
    send_count = {}
    dst_name = 'ibr-' + str(dst_host + 1)
    command = ""
    dir_path = BASE_PATH + "rec/"
    if not os.path.isdir(dir_path): os.makedirs(dir_path)
    for src in src_hosts:
        src_index = src[0]
        src_name = 'ibr-' + str(src_index + 1)
        if not send_count.has_key(src_name):
            send_count[src_name] = 1
        src_dst_num = src_name + "_" + dst_name +\
                  "_" + str(send_count[src_name])
        command = command + '/usr/local/bin/dtnrecv --name ' + src_dst_num +\
               " --file " + dir_path + src_dst_num + ".txt & "
        send_count[src_name] = send_count[src_name] + 1
    return command

def create_file(file_path, content, size):
    '''size unit is Bytes'''
    content = content + '\n'
    left_content = ''
    cnt = size/len(content)
    if size%len(content): left_content = '1'*(size%len(content))
    
    dir_path = os.path.dirname(file_path)
    if not os.path.isdir(dir_path): os.makedirs(dir_path)
    
    with open(file_path, 'w') as file_obj:
        for i in range(cnt):
            file_obj.write(content)
        if left_content: file_obj.write(left_content)


def create_node_send_command(src_host, dst_hosts):
    '''src_host is list index, start from 0,
       src_host is the host sending dtn
       dst_hosts is list [[host_index, time_index], [],...]
    '''
    send_count = {}
    src_name = 'ibr-' + str(src_host + 1)
    command = ""
    i = 0
    time_count = 0
    while i < len(dst_hosts):
        dst = dst_hosts[i]
        time_index = dst[1]
        if time_count >= time_index:
            dst_index = dst[0]
            dst_name = 'ibr-' + str(dst_index + 1)
            if not send_count.has_key(dst_name):
                send_count[dst_name] = 1
            src_dst_num = src_name + "_" + dst_name +\
                          "_" + str(send_count[dst_name])
            file_path = BASE_PATH + 'send/' + src_dst_num + '.txt'
            create_file(file_path, src_dst_num, 1024)
    
    
            cmd = '/usr/local/bin/dtnsend dtn://' + dst_name + '/' + src_dst_num +\
                  ' ' + file_path + ' &'
            send_count[dst_name] = send_count[dst_name] + 1
            i = i + 1
            time_count = time_count + 1
            yield cmd
            
        time_count = time_count + 1
        yield ""
    
def setup_dtnd(host_num, hosts2ports):
    name = 'ibr-' + str(host_num)
    port_id = hosts2ports[name][0]
    interface =  'ns' + port_id[:11]
    start_cmd = "/usr/local/sbin/dtnd -c /etc/ibrdtn/ibrdtnd.conf -i %s &"
    print start_cmd % (interface, )
    if os.system(start_cmd % (interface,)):
        error_str = 'Failed: ' + start_cmd 
        log_error(host_num, error_str)
        sys.exit(-1)
    

def ibr_rec_send(host_num, hosts2ports, receivers, senders):
    rec_cmd = create_node_rec_command(host_num-1, receivers) 
    if os.system(rec_cmd): 
        error_str = 'Failed: ' + rec_cmd 
        log_error(host_num, error_str)
        sys.exit(-1)
    
    send_cmd_iter = create_node_send_command(host_num-1, senders)
    while True:
        try:
            send_cmd = send_cmd_iter.next()
            if os.system(send_cmd): 
                rror_str = 'Failed: ' + send_cmd 
                log_error(host_num, error_str)
                sys.exit(-1)
            yield True
        except StopIteration:
            break
    yield False

def main():
    try:
        start_time = float(sys.argv[1])
        warm_time = int(sys.argv[2])
        time_unit = int(sys.argv[3])
    except:
        help_info = "Usage:%s <start_time> <warm_time> <time_unit>(s)\n" % sys.argv[0]
        sys.exit(-1)
    
    base_path = "/tmp/"

    while True:
        host_num = get_host_num(base_path)
        if host_num < 0:
            time.sleep(1)
        else:
            break
    print "Obtain host_num:%d" % (host_num,)

    if os.system('/usr/bin/killdtn &'):
        log_error(host_num, 'Failed: /usr/bin/killdtn')
        sys.exit(-1) 

    path = base_path + 'cgr_l.' + str(host_num) 
    with open(path, 'rb') as f:
        cgr_l =  pickle.load(f)
    print "Loaded %s!" % path    

    path = base_path + 'senders.' + str(host_num) 
    with open(path, 'rb') as f:
        senders =  pickle.load(f)
    print "Loaded %s!" % path    

    path = base_path + 'receivers.' + str(host_num) 
    with open(path, 'rb') as f:
        receivers =  pickle.load(f)
    print "Loaded %s!" % path    
  
    path = base_path + 'hosts2ports' 
    with open(path, 'rb') as f:
        hosts2ports =  pickle.load(f)
    print "Loaded %s!" % path    

    init(host_num, hosts2ports)
    print "Finished to init"

    print "Waiting for starting"
    while time.time() < start_time: 
        time.sleep(0.1)
        
    print "Start now!!!"
    print "Setup dtnd,Warm-up  now!!!"
    setup_dtnd(host_num, hosts2ports)
    start_time = start_time + warm_time
    while time.time() < (start_time):
        time.sleep(0.1)

    topology_iter = topology_ctl(host_num, cgr_l, hosts2ports) 
    rec_send_iter = ibr_rec_send(host_num, hosts2ports, receivers, senders)
    rec_send_flag = True
    count = 0
    while True:
        count = count +1
        next_time = start_time + time_unit*count
        try:
            topology_iter.next()
        except:
            break
        
        rec_send_iter.next()
        if rec_send_flag:
            try:
                rec_send_flag = rec_send_iter.next()
            except:
                pass
            
        while time.time() < next_time: 
            time.sleep(0.1)
        #print time.time(), count
        
if __name__ == '__main__':
    sys.exit(main())
    
