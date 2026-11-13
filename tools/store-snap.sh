#!/bin/bash
# M4-① 当期商店每日常规快照 v2(2026-11-11 加深:两级爬取)
# v1: 主页+主页目录页;v2: 目录页内再发现目录页(并集封顶 40 页),仍每日 04:57
# 供未来活动考证「当期商店长什么样」;存运维区不公开(web 根外),365 天滚动
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"
BASE=/opt/services/wtevents-ops/store
DAY=$(date +%F)
DIR=$BASE/$DAY
mkdir -p "$DIR"
curl -sf --max-time 30 -A "$UA" -L https://store.gaijin.net/ -o "$DIR/index.html" || { echo "$DAY FAIL main" >> /opt/services/wtevents-ops/store-snap.log; exit 1; }
links() { grep -oE 'store.gaijin.net/catalog.php[^"<]*' "$1" 2>/dev/null | sed 's/&amp;/\&/g' | sort -u; }
mapfile -t TODO < <(links "$DIR/index.html")
declare -A DONE=()
fetched=0
while [ ${#TODO[@]} -gt 0 ] && [ $fetched -lt 40 ]; do
  u="${TODO[0]}"
  TODO=("${TODO[@]:1}")
  [ -n "${DONE[$u]:-}" ] && continue
  DONE["$u"]=1
  n=$(echo "$u" | md5sum | cut -c1-8)
  if curl -sf --max-time 20 -A "$UA" -L "https://$u" -o "$DIR/catalog-$n.html" 2>/dev/null; then
    fetched=$((fetched+1))
    while IFS= read -r nu; do
      [ -z "${DONE[$nu]:-}" ] && TODO+=("$nu")
    done < <(links "$DIR/catalog-$n.html")
  fi
  sleep 2
done
gzip -f "$DIR"/*.html 2>/dev/null
find $BASE -maxdepth 1 -type d -name '20*' -mtime +365 -exec rm -rf {} + 2>/dev/null
echo "$(date '+%F %T') [store-snap] $DAY: $(ls "$DIR" | wc -l) files $(du -sh "$DIR" | cut -f1) (v2 two-level)" >> /opt/services/wtevents-ops/store-snap.log
