#!/bin/bash
# 全部のインスタンスのうち、resultsにないものを実行して記録する
# timeoutはエラーはいてもOKだけどほかのエラーは困る
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
    touch results/${t}_${count}.csv
    timeout 1800 python3 solve_ISR.py "${graphpath}" "${solpath}" "${t}" "${count}" > results/${t}_${count}.csv
    #python3 make_csv_from_log.py "${t}_${count}"
    echo "results/${graph}_${sol}.csv"
  fi
  ((count++))
done < 2022benchmark-main/list/list-all-benchmark.csv