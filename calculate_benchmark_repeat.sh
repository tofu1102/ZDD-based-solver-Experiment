#!/bin/bash
# 全部のインスタンスのうち、resultsにないものを実行して記録する
# timeoutはエラーはいてもOKだけどほかのエラーは困る

while read row; do
  graph=`echo ${row} | cut -d , -f 1`
  sol=`echo ${row} | cut -d , -f 2`
  graph="2022benchmark-main/${graph}"
  sol="2022benchmark-main/${sol}"
  graphpath="${graph}"
  solpath="${sol}"
  graph=${graph//\//_}
  sol=${sol//\//_}
  graph=${graph//./_}
  sol=${sol//./_}
  
  
  if [ -e "results/${graph}_${sol}.csv" ]; then
    :
  else
    python3 solve_ISR.py "${graphpath}" "${solpath}" "${graph}_${sol}"
    python3 make_csv_from_log.py
    echo "results/${graph}_${sol}.csv"
  fi
done < 2022benchmark-main/list/list-all-benchmark.csv