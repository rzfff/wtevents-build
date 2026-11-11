#!/bin/bash
# M4-① 当期商店每日常规快照(2026-11-11 上线):Gaijin 商店主页+当日发现的目录页,按日落盘 gz
# 供未来活动考证「当期商店长什么样」;存运维区不公开(store/ 在 wtevents-ops 下,web 根外)
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"
BASE=/opt/services/wtevents-ops/store
DAY=$(date +%F)
DIR=$BASE/$DAY
mkdir -p "$DIR"
curl -sf --max-time 30 -A "$UA" -L https://store.gaijin.net/ -o "$DIR/index.html" || { echo "$DAY FAIL main" >> /opt/services/wtevents-ops/store-snap.log; exit 1; }
grep -oE 'store.gaijin.net/catalog.php[^"<]*' "$DIR/index.html" | sed 's/&amp;/\&/g' | sort -u | head -24 | while read -r u; do
  n=$(echo "$u" | md5sum | cut -c1-8)
  curl -sf --max-time 20 -A "$UA" -L "https://$u" -o "$DIR/catalog-$n.html" 2>/dev/null || true
  sleep 2
done
gzip -f "$DIR"/*.html 2>/dev/null
find $BASE -maxdepth 1 -type d -name '20*' -mtime +365 -exec rm -rf {} + 2>/dev/null
echo "$(date '+%F %T') [store-snap] $DAY: $(ls "$DIR" | wc -l) files $(du -sh "$DIR" | cut -f1)" >> /opt/services/wtevents-ops/store-snap.log
