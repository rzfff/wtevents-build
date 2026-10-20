#!/bin/bash
# wtevents M2 list-page fetcher — run on anhappy server
mkdir -p /tmp/wte/lists
cd /tmp/wte || exit 1
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"
fails=0
for i in $(seq 1 365); do
  f="lists/en_p$i.html"
  if [ ! -s "$f" ]; then
    curl -s --max-time 25 -A "$UA" -o "$f" "https://warthunder.com/en/news/page/$i/" || { fails=$((fails+1)); echo "FAIL en_p$i"; }
    sleep 0.25
  fi
done
for i in $(seq 1 128); do
  f="lists/zh_p$i.html"
  if [ ! -s "$f" ]; then
    curl -s --max-time 25 -A "$UA" -o "$f" "https://warthunder.com/zh/news/page/$i/" || { fails=$((fails+1)); echo "FAIL zh_p$i"; }
    sleep 0.25
  fi
done
tar czf lists.tgz -C lists .
echo "LISTS_DONE files=$(ls lists | wc -l) fails=$fails size=$(du -h lists.tgz | cut -f1)"
