#!/bin/bash

file=`curl -s -D - http://kaibro.tw/hw0/hw0.php | grep Location | awk '{print $2}' | tr -d '\r'`
curl http://kaibro.tw/hw0/$file
