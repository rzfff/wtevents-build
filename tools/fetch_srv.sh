#!/bin/bash
# wtevents M1 article fetcher — run on anhappy server
mkdir -p /tmp/wte/art
cd /tmp/wte || exit 1
tr -d '\r' < fetch_en.tsv > en.clean
tr -d '\r' < fetch_zh.txt > zh.clean
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"
fails=0
while IFS=$'\t' read -r id url; do
  case "$id" in ''|x) continue;; esac
  f="art/en_${id}.html"
  if [ ! -s "$f" ]; then
    curl -s --max-time 25 -A "$UA" -o "$f" "$url" || { echo "FAIL en $id"; fails=$((fails+1)); }
    sleep 0.3
  fi
done < en.clean
while read -r url; do
  case "$url" in
    */news/*) id=$(echo "$url" | sed 's#.*/news/\([0-9]*\).*#\1#');;
    *) continue;;
  esac
  f="art/zh_${id}.html"
  if [ ! -s "$f" ]; then
    curl -s --max-time 25 -A "$UA" -o "$f" "$url" || { echo "FAIL zh $id"; fails=$((fails+1)); }
    sleep 0.3
  fi
done < zh.clean
tar czf art.tgz -C art .
echo "FETCH_DONE files=$(ls art | wc -l) fails=$fails size=$(du -h art.tgz | cut -f1)"
