#!/bin/bash
# wtevents M3 Wayback snapshot fetcher — run on anhappy server
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"
cd /tmp/wte/wb || exit 1
mkdir -p snap
worker(){
  while read -r line; do
    url=$(echo "$line" | awk '{print $1}')
    dt=$(echo "$line" | awk '{print $2}')
    ts=$(echo "$url" | sed 's#.*/web/\([0-9]\{14\}\)/.*#\1#')
    cat=$(echo "$url" | sed 's#.*category=\([A-Za-z]*\).*#\1#')
    f="snap/${cat}_${ts}.html"
    if [ ! -s "$f" ]; then
      curl -sL --max-time 40 -A "$UA" -o "$f" "$url" || { rm -f "$f"; echo "FAIL $cat $ts"; }
      sleep 0.5
    fi
  done
}
cat tm_WarThunderPacks.txt tm_SpecOffers.txt tm_GoldenEagles.txt tm_PremiumAccount.txt > all.txt
wc -l < all.txt
worker < all.txt
echo "WB_DONE files=$(ls snap | wc -l)"
tar czf wb_snap.tgz -C snap .
echo "WB_TGZ $(du -h wb_snap.tgz | cut -f1)"
