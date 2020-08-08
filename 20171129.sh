#!/bin/bash
if [ "$#" -eq 1 ]; then
  python3 20171129_2.py "$*" > 20171129_2.txt
  exit 0
fi

if [ "$#" -eq 2 ]; then
  python3 20171129_1.py $1 $2 > 20171129_1.txt
  exit 0
fi