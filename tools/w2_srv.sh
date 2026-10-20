#!/bin/bash
# extra fetch worker — eats the tail slices alongside the main fetcher
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"
while IFS=$'\t' read -r id url; do
  case "$id" in ''|x) continue;; esac
  f="/tmp/wte/art2/en_${id}.html"
  if [ ! -s "$f" ]; then
    curl -s --max-time 25 -A "$UA" -o "$f" "$url" || echo "FAIL en $id"
    sleep 0.3
  fi
done < /tmp/wte/en2.tail
while read -r url; do
  case "$url" in
    */news/*) id=$(echo "$url" | sed 's#.*/news/\([0-9]*\).*#\1#');;
    *) continue;;
  esac
  f="/tmp/wte/art2/zh_${id}.html"
  if [ ! -s "$f" ]; then
    curl -s --max-time 25 -A "$UA" -o "$f" "$url" || echo "FAIL zh $id"
    sleep 0.3
  fi
done < /tmp/wte/zh2.tail
echo WORKER_DONE
