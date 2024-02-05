#!/bin/bash

# resultsフォルダ内のファイル名を出力する
for file in results/*; do
  python3 remove_bugfile.py "$file"
  python3 analyze_reconf_time.py "$file" >> reconf_time-zdd.csv
done
