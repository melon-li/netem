#!/bin/bash
for name in `ip netns`
do
echo $name
sudo docker exec -d $name ionstart -I /root/ion-3.3.1/ion-open-source/configs/loopback-ltp/loopback_ltp.rc
sleep 3
done

