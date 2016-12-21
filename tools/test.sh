#!/bin/bash
function test(){
echo '1'> test.txt
}

test &
sleep 1
cat test.txt
