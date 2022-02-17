#!/bin/bash

YELOW='\033[1;33m'
LBLUE='\033[1;34m'
REDDD='\033[0;31m'
GREEN='\033[0;32m'
CLEAR='\033[0m'
PATTERN='serial-log.py'

PROCESS_IDS=$(pgrep -f ${PATTERN})

for i in $(echo "$PROCESS_IDS" | tr "\n" " ")
do
  COMD=$(ps -p "$i" -o command | awk '{print $3}' | tr "\n" " ")
  echo -e "${YELOW}Stopping ${REDDD}${i}${CLEAR} -${LBLUE}${COMD}${CLEAR}"
  kill -6 "$i"
done

echo -e "\n${GREEN}All logging processes have been stopped successfully!\n${CLEAR}"

cd Log || exit
python3 plot.py
