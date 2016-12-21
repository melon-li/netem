#!/bin/bash
s2='\tinclude ion_config'
s3='}'
s22='\t\tpath => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:",'
s23='\t}'

cur=`date +%s`
cur=$((cur+10))
for i in `seq 1 55`
do
    cur=$((cur+3))
    echo -e "node \"ibr-$i\"{"
    echo -e "\texec {'te $cur \"ionstart -I /root/ion-3.3.1/ion-open-source/configs/loopback-ltp/loopback_ltp.rc\"':"
    echo -e $s22
    echo -e $s23
    echo -e $s3
done

for i in `seq 1 45`
do
    cur=$((cur+3))
    echo -e "node \"ibr2-$i\"{"
    echo -e "\texec {'te $cur \"ionstart -I /root/ion-3.3.1/ion-open-source/configs/loopback-ltp/loopback_ltp.rc\"':"
    echo -e $s22
    echo -e $s23
    echo -e $s3
done

exit 0

for i in `seq 1 55`
do
    echo -n "ibr-$i "
done
for i in `seq 1 45`
do
    echo -n "ibr2-$i "
done

exit 0
for i in `seq 1 55`
do
    echo -e "node \"ibr-$i\"{"
    echo -e $s2
    echo -e $s3
done

for i in `seq 1 45`
do
    echo -e "node \"ibr2-$i\"{"
    echo -e $s2
    echo -e $s3
done

