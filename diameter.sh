#!/bin/bash

count=0
while read row; do
  graph=`echo ${row} | cut -d , -f 1`
  sol=`echo ${row} | cut -d , -f 2`
  graph="2022benchmark-main/${graph}"
  sol="2022benchmark-main/${sol}"
  graphpath="${graph}"
  solpath="${sol}"
  
  
  
  timeout 3600 python3 diameter.py "${graphpath}" "${solpath}" "${count}"
  echo "${count}"
  ((count++))
done < 2022benchmark-main/list/list-all-benchmark.csv