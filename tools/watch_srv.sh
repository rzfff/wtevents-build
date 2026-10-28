#!/bin/bash
# wtevents 增量哨兵 v3+annotate — cron 每日 04:53
STATE=/opt/services/wtevents-ops/watch
LOG=/opt/services/wtevents-ops/watch.log
mkdir -p "$STATE"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"
say(){ echo "$(date '+%F %T') $*" >> "$LOG"; }

# 1) zh/en 新闻列表页 URL 集合 diff(前 2 页)
for L in en zh; do
  : > "$STATE/list_$L.new"
  for PG in "" "?page=2"; do
    curl -sf --max-time 30 -A "$UA" "https://warthunder.com/$L/news/$PG" | grep -o "/$L/news/[0-9][^\"]*" >> "$STATE/list_$L.tmp" 2>/dev/null
    sort -u "$STATE/list_$L.tmp" > "$STATE/list_$L.new" && rm -f "$STATE/list_$L.tmp"
    sleep 0.5
  done
  if [ -s "$STATE/list_$L.new" ]; then
    if [ -f "$STATE/list_$L.txt" ]; then
      NEWN=$(comm -23 "$STATE/list_$L.new" "$STATE/list_$L.txt" | grep -vc '^$')
      if [ "$NEWN" -gt 0 ]; then
        say "[$L] 新文章 $NEWN 篇: $(comm -23 "$STATE/list_$L.new" "$STATE/list_$L.txt" | grep -v '#' | head -3 | tr '\n' ' ')"
      fi
    fi
    cmp -s "$STATE/list_$L.new" "$STATE/list_$L.txt" || cp "$STATE/list_$L.new" "$STATE/list_$L.txt"
  fi
done

# 2) timelapse
curl -sf --max-time 30 -A "$UA" "https://wiki.warthunder.com/history_timelapse" -o "$STATE/tl.new"
if [ -s "$STATE/tl.new" ] && grep -q "history_timelapse\|regular_event" "$STATE/tl.new"; then
  H=$(md5sum < "$STATE/tl.new" | cut -d' ' -f1)
  O=$(cat "$STATE/tl.md5" 2>/dev/null)
  if [ "$H" != "$O" ]; then
    say "[timelapse] 骨架有更新(md5 $H)——重跑 build_base.py 对账防漏"
    echo "$H" > "$STATE/tl.md5"
  fi
fi

# 3) datamine
UP=$(curl -sf --max-time 10 "https://raw.githubusercontent.com/gszabi99/War-Thunder-Datamine/master/version" 2>/dev/null | tr -d '[:space:]')
CUR=$(readlink /opt/services/wtapi/current 2>/dev/null | grep -o '2\.[0-9.]*' | head -1)
if [ -n "$UP" ] && [ -n "$CUR" ] && [ "$UP" != "$CUR" ]; then
  say "[datamine] 上游 $UP ≠ 在役 $CUR(wtapi 换版后 wtevents 车池也应重跑)"
fi

# 4) wtstats 新鲜度
CUR_DATA=$(readlink /opt/services/wtstats/data-current 2>/dev/null)
if [ -n "$CUR_DATA" ]; then
  AGE=$(( ($(date +%s) - $(stat -c %Y "$CUR_DATA")) / 86400 ))
  if [ "$AGE" -ge 4 ]; then
    say "[wtstats] 数据版本已 $AGE 天未换(上游 3 天一推)——疑似更新链路故障"
  fi
fi

# 5) 标注:哪些基线文章不在 events.json 中(真正需要处理的)
python3 /opt/services/wtevents-ops/watch_annotate.py 2>/dev/null

# 自检
if [ -f "$STATE/list_en.txt" ] && [ "$(find "$STATE/list_en.txt" -mtime +7 | wc -l)" -gt 0 ]; then
  say "[check] EN 列表 7 天零变化,检查哨兵与官方站是否异常"
fi
