#!/bin/bash
# wtevents M2 article fetcher — run on anhappy server (art2, resume-safe)
mkdir -p /tmp/wte/art2
cd /tmp/wte || exit 1
tr -d '\r' < fetch2_en.tsv > en2.clean
tr -d '\r' < fetch2_zh.txt > zh2.clean
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"
fails=0
while IFS=$'\t' read -r id url; do
  case "$id" in ''|x) continue;; esac
  f="art2/en_${id}.html"
  if [ ! -s "$f" ]; then
    curl -s --max-time 25 -A "$UA" -o "$f" "$url" || { echo "FAIL en $id"; fails=$((fails+1)); }
    sleep 0.25
  fi
done < en2.clean
while read -r url; do
  case "$url" in
    */news/*) id=$(echo "$url" | sed 's#.*/news/\([0-9]*\).*#\1#');;
    *) continue;;
  esac
  f="art2/zh_${id}.html"
  if [ ! -s "$f" ]; then
    curl -s --max-time 25 -A "$UA" -o "$f" "$url" || { echo "FAIL zh $id"; fails=$((fails+1)); }
    sleep 0.25
  fi
done < zh2.clean
tar czf art2.tgz -C art2 .
echo "FETCH2_DONE files=$(ls art2 | wc -l) fails=$fails size=$(du -h art2.tgz | cut -f1)"
