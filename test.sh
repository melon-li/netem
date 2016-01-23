#!/bin/bash
#while [ 1 ]
#do
#    sleep 0.01
#done

ip_base="10.0.0."
for i in `seq 56`
do
     num=i
     ip=$ip_base"$i/32"
#     echo  $ip
#    tc qdisc change dev eth0 root netem delay $i'ms'
     iptables -I INPUT -i eth0 -p ip --src $ip -j ACCEPT
done

