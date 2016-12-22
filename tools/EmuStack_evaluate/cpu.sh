#!/bin/bash
function cpu100(){
    while [[ 1 ]]
    do
        s=1
    done
}

for i in `seq $1`
do
    cpu100 &
done
