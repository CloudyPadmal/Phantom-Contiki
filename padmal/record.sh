#!/bin/bash

YELOW='\033[1;33m'
REDDD='\033[0;31m'
GREEN='\033[0;32m'
CLEAR='\033[0m'

if [ -d "Log" ]; then
  fileDir="$(date +"%F:%I-%M-%S")"
  mv Log "${fileDir}"
  echo -e "\n${YELOW}Log file renamed to" "${REDDD}${fileDir}${YELOW}" "!${CLEAR}"
fi

cp -r _Log Log

echo -e "${GREEN}Logging started!${CLEAR}\n"

python3 serial-log.py "$NODE_RX" Log/Receive.txt &
python3 serial-log.py "$NODE_E1" Log/Eaves-1.txt &
python3 serial-log.py "$NODE_E2" Log/Eaves-2.txt &
python3 serial-log.py "$NODE_E3" Log/Eaves-3.txt &
python3 serial-log.py "$NODE_E4" Log/Eaves-4.txt &
python3 serial-log.py "$NODE_TX"