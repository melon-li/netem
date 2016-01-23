#/usr/bin/env python
#coding:utf-8
import os
import sys
import time
import cPickle as pickle

def get_host_num(path)
    files = os.listdir(path)
    for name in files:
        if name.find('cgr_l') >= 0: 
            pos = name.find('.') + 1
            return int(name[pos:])
    return -1

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
        for index, state in enumerate(cgr_r):
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
    for src in src_hosts:
        src_index = src[0]
        src_name = 'ibr-' + str(src_index + 1)
        if not send_count.has_key(src_name):
            send_count[src_name] = 1
        src_dst_num = src_name + "_" + dst_name +\
                  "_" + str(send_count[src_name])
        command = command + '/usr/local/bin/dtnrecv --name ' + src_dst_num +\
               " --file /root/exp/ibr/rec/" + src_dst_num + ".txt & "
        send_count[src_name] = send_count[src_name] + 1
    return command

def create_node_send_command(src_host, dst_hosts, time_unit, time_after):
    '''src_host is list index, start from 0,
       src_host is the host sending dtn
       dst_hosts is list [[host_index, time_index], [],...]
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


def ibr_rec_send(host_num, receivers, senders, time_count):
    name = 'ibr-' + str(host_num)
    port_id = hosts2ports[name][0]
    interface =  'ns' + port_id[:11]

    start_cmd = "/usr/local/bin/dtnd -c /etc/ibrdtn/ibrdtnd.conf -i %s &"
    if os.system(start_cmd % (interface,)): sys.exit(-1)

    rec_cmd = create_node_rec_command(host_num-1, src_hosts) 
    if os.system(rec_cmd): sys.exit(-1)
    
    i = 0
    while i < len(senders):
        dst = senders[i]
        if time_count >= dst[1]:
            dst_index = dst[0]
            dst_name = 'ibr-' + str(dst_index + 1)
            if 
            src_dst_num = name + "_" + dst_name +\
                          "_" + str(send_count[dst_name])

            send_cmd = "usr/local/bin/dtnsend dtn://"
    

def main():
    try:
        start_time = int(sys.argv[1])
        time_unit = int(sys.argv[2])
    except:
        help_info = "Usage:%s <start_timestamp> <time_unit>(s)\n" % sys.argv[0]
        sys.exit(-1)
    
    base_path = "/tmp/"
    start_time = a
    while True:
        host_num = get_host_num(base_path)
        if host_num < 0:
            time.sleep(1)
        else:
            break
    path = base_path + 'cgr_l.' + str(host_num) 
    with open(path, 'rb') as f:
        cgr_l =  pickle.load(f)

    path = base_path + 'senders.' + str(host_num) 
    with open(path, 'rb') as f:
        senders =  pickle.load(f)

    path = base_path + 'receivers.' + str(host_num) 
    with open(path, 'rb') as f:
        receivers =  pickle.load(f)
  
    path = base_path + 'hosts2ports' 
    with open(path, 'rb') as f:
        hosts2ports =  pickle.load(f)

    while time.time() < start_time: 
        time.sleep(0.1)

     topologytopology_ctl(cgr, hosts2ports) 
    for cgr in cgr_l:
        next_time = start_time + time_unit
        while time.time() < next_time: 
            time.sleep(0.1)
        

    
