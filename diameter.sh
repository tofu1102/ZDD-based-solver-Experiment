#!/bin/bash

count=0
t=$1
while read row; do
  graph=`echo ${row} | cut -d , -f 1`
  sol=`echo ${row} | cut -d , -f 2`
  graph="2022benchmark-main/${graph}"
  sol="2022benchmark-main/${sol}"
  graphpath="${graph}"
  solpath="${sol}"
  
  
  if [ -e "results/${t}_${count}.csv" ]; then
    :
  else
    timeout 3600 python3 diameter.py "${graphpath}" "${solpath}" "${count}" >> diameter.txt
    #python3 make_csv_from_log.py "${t}_${count}"
    echo "${count}"
  fi
  ((count++))
done < 2022benchmark-main/list/list-all-benchmark.csv