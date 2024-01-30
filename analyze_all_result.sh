#!/bin/bash

# resultsフォルダ内のファイル名を出力する
for file in results/*; do
  python3 remove_bugfile.py "$file"
  python3 analyze.py "$file" >> result.csv
done
