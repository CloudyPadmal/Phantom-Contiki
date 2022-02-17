#!/bin/bash

PATTERN='python3 serial-log.py'

status=$(pgrep -f "${PATTERN}")

for i in $status
do
   kill -6 "$i"
done

cd Log
python3 plot.py
