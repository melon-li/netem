#!/bin/bash
live=`sudo docker ps --no-trunc| grep docker| awk -F" " '{print $1}'`

names=`ip netns`
num=0
for l in `echo $live`
do
    num=$(($num+1))
done
echo $num
echo "Started deleting poweroff container"
for n in `echo $names`
do
    cnt=0
    for l in `echo $live`
    do
        if [[ "$n" == "$l" ]];then
            break
        fi
        cnt=$((cnt+1))
    done
   #echo $cnt
   if [[ $cnt -ge $num ]];then
       echo "Deleting namespance "$n
       sudo ip netns del $n
   fi
done
echo "Finished deleting poweroff container"
