#!/bin/bash

last_is_left=0
touch /tmp/csie_$$
tail -F /tmp/csie_$$ | nc csie.ctf.tw 10123 | while read line
do
    if [ $last_is_left -eq 1 ]
    then

        echo $line |  tr ' ' '\n' | sort -n | tr '\n' ' ' >> /tmp/csie_$$
        echo >> /tmp/csie_$$
    fi
    [ -n "`echo $line | grep 'times left'`" ] && last_is_left=1 && echo $line || last_is_left=0
    echo $line | grep -i flag
    [ -n "`echo $line | grep -i 'flag{'`" ] && kill `ps aux | grep 'tail -F /tmp/csie_' | grep -v grep | awk '{print $2}'`
done
rm /tmp/csie_$$
# hum? you say this is a pwntools practice?
