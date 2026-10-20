/* wtevents M1 — 战雷活动总览(数据:./data/events.json) */
'use strict';

const TYPE_META = {
  sale:     {zh:'促销折扣', cls:'t-sale'},
  marathon: {zh:'马拉松任务', cls:'t-marathon'},
  craft:    {zh:'拼装活动', cls:'t-craft'},
  battlepass:{zh:'战斗通行证', cls:'t-bp'},
  festive:  {zh:'节日活动', cls:'t-festive'},
  anniversary:{zh:'周年庆', cls:'t-anniv'},
  april:    {zh:'愚人节', cls:'t-april'},
  worldwar: {zh:'世界大战', cls:'t-ww'},
  special:  {zh:'特别活动', cls:'t-special'},
  market:   {zh:'市场联动', cls:'t-market'},
  memorial: {zh:'纪念日', cls:'t-memorial'},
};
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

let EVENTS = [], state = {type:'all', q:''};

function fmtDate(iso){
  if(!iso) return '?';
  const d = new Date(iso);
  if(isNaN(d)) return esc(iso);
  // 存 UTC;渲染北京时间(活动跨 11:00 GMT 开结,北京时间同日 19:00)
  const b = new Date(d.getTime() + 8*3600*1000);
  const p = n => String(n).padStart(2,'0');
  let s = `${b.getUTCFullYear()}-${p(b.getUTCMonth()+1)}-${p(b.getUTCDate())}`;
  if(/T/.test(iso) && /:\d\d/.test(iso) && !iso.endsWith('T00:00:00Z')) s += ` ${p(b.getUTCHours())}:${p(b.getUTCMinutes())}`;
  return s;
}
function durDays(a,b){
  if(!a||!b) return null;
  return Math.round((new Date(b)-new Date(a))/86400000);
}

function render(){
  const tl = $('#timeline');
  const q = state.q.trim().toLowerCase();
  const evs = EVENTS.filter(e=>{
    if(state.type!=='all' && e.type!==state.type) return false;
    if(!q) return true;
    const hay = [e.name_zh,e.name_en,e.type, ...(e.vehicles||[]).map(v=>(v.name_zh||'')+' '+(v.name_en||'')), ...(e.awards||[])].filter(x=>x&&x!=='null').join(' ').toLowerCase();
    return hay.includes(q);
  });
  $('#empty').hidden = evs.length>0;
  const byYear = {};
  evs.forEach(e=>{ (byYear[(e.start||'????').slice(0,4)] ||= []).push(e); });
  const years = Object.keys(byYear).sort((a,b)=>b-a);
  let html = '';
  for(const y of years){
    html += `<div class="year-h" id="Y${y}"><h2>${y}</h2><span class="cnt">${byYear[y].length} 项</span></div><div class="grid">`;
    for(const e of byYear[y].sort((a,b)=>(b.start||'').localeCompare(a.start||''))) html += card(e);
    html += '</div>';
  }
  tl.innerHTML = html;
  tl.querySelectorAll('.ev').forEach(el=>el.addEventListener('click',()=>openDrawer(el.dataset.id)));
}

function card(e){
  const tm = TYPE_META[e.type] || TYPE_META.special;
  const color = `var(--${tm.cls})`;
  const veh = e.vehicles||[];
  const thumbs = veh.slice(0,4).map(v=>`<img loading="lazy" src="${esc(v.image)}" alt="${esc(v.name_zh||v.name_en)}" onerror="this.style.display='none'">`).join('')
    + (veh.length>4?`<span class="more">+${veh.length-4}</span>`:'');
  const dcount = (e.discounts||[]).length;
  const dline = !veh.length && dcount ? `<div class="thumbs"><span class="more">🛒 ${dcount} 项折扣</span></div>` : '';
  const bp = e.bp_season?`第 ${e.bp_season} 季 · `:'';
  const d = durDays(e.start,e.end);
  return `<div class="ev" data-id="${esc(e.id)}">
    <div class="row1">
      <span class="badge" style="background:${color}">${esc(tm.zh)}</span>
      <span class="date">${fmtDate(e.start)} ~ ${fmtDate(e.end)}${d!=null?` · ${d}天`:''}</span>
    </div>
    <div class="name">${esc(e.name_zh||e.name_en)}<span class="en">${bp}${esc(e.name_en)}</span></div>
    ${thumbs?`<div class="thumbs">${thumbs}</div>`:dline}
  </div>`;
}

function openDrawer(id){
  const e = EVENTS.find(x=>x.id===id); if(!e) return;
  const tm = TYPE_META[e.type] || TYPE_META.special;
  const veh = e.vehicles||[];
  const conf = e.confidence>=0.85?'三源核实':(e.confidence>=0.6?'双源':'单源/推断');
  let h = `<div class="d-type" style="color:var(--${tm.cls})">${esc(tm.zh)}${e.bp_season?` · 第 ${e.bp_season} 季`:''}</div>
    <div class="d-title">${esc(e.name_zh||e.name_en)}</div>
    ${e.name_zh&&e.name_en?`<div class="d-en">${esc(e.name_en)}</div>`:''}
    <div class="d-dates"><b>${fmtDate(e.start)}</b> ~ <b>${fmtDate(e.end)}</b>(北京时间)
      ${e.end_raw?`<div class="d-note">原文:${esc(e.end_raw)}</div>`:''}</div>`;
  if(e.deadlines && e.deadlines.length){
    h += `<div class="d-sec">关键节点</div><ul class="dead">` + e.deadlines.map(x=>`<li>${esc(x.what)} — ${fmtDate(x.when) || esc(x.when)}</li>`).join('') + '</ul>';
  }
  if(e.discounts && e.discounts.length){
    h += `<div class="d-sec">折扣</div><table class="dis"><tr><th>对象</th><th>折扣</th><th>说明</th></tr>`
      + e.discounts.map(x=>{
          const pct = x.percent!=null ? ('-'+esc(String(x.percent))+'%') : esc(x.note||'');
          const desc = (x.percent!=null ? [x.item,x.note] : [x.item||x.note]).filter(Boolean).join(' — ');
          return `<tr><td>${esc(x.target)}</td><td class="pct">${pct}</td><td class="d-note">${esc(desc)}</td></tr>`;
        }).join('') + '</table>';
  }
  if(e.tasks) h += `<div class="d-sec">怎么拿</div><div class="tasks">${esc(e.tasks)}</div>`;
  if(veh.length){
    h += `<div class="d-sec">奖励载具(${veh.length})</div><div class="veh-grid">` + veh.map(v=>
      `<div class="veh"><img loading="lazy" src="${esc(v.image)}" onerror="this.style.visibility='hidden'">
       <div class="vn">${esc(v.name_zh||v.name_en)}</div><div class="ve">${esc(v.name_en)}</div></div>`).join('') + '</div>';
  } else if(e.awards && e.awards.length){
    h += `<div class="d-sec">奖励(官方年表记载)</div><ul class="dead">` + e.awards.map(a=>`<li>${esc(a)}</li>`).join('') + '</ul>';
  }
  if(e.sub_events && e.sub_events.length){
    h += `<div class="d-sec">同期子活动</div><ul class="dead">` + e.sub_events.map(s=>`<li>${esc(s.title)}(${esc(s.start||'?')} ~ ${esc(s.end||'?')})</li>`).join('') + '</ul>';
  }
  if(e.notes) h += `<div class="d-note" style="margin-top:14px">${esc(e.notes)}</div>`;
  const srcs = [];
  const enS = e.sources&&e.sources.en, zhS = e.sources&&e.sources.zh;
  (Array.isArray(enS)?enS.slice(0,3):enS?[enS]:[]).forEach((u,i)=>srcs.push(`<a href="${esc(u)}" target="_blank" rel="noopener">官方新闻(EN)${Array.isArray(enS)&&enS.length>1?('·'+(i+1)):''}</a>`));
  (Array.isArray(zhS)?zhS.slice(0,2):zhS?[zhS]:[]).forEach(u=>srcs.push(`<a href="${esc(u)}" target="_blank" rel="noopener">官方新闻(中文)</a>`));
  if(e.sources&&e.sources.wiki) srcs.push(`<a href="${esc(e.sources.wiki)}" target="_blank" rel="noopener">官方 Wiki</a>`);
  if(srcs.length) h += `<div class="d-sec">来源${e.confidence!=null?`<span class="conf">${conf}</span>`:''}</div><div class="srcs">${srcs.join('')}</div>`;
  $('#drawer-body').innerHTML = h;
  $('#drawer').hidden = false; $('#scrim').hidden = false;
  document.body.style.overflow = 'hidden';
}
function closeDrawer(){ $('#drawer').hidden = true; $('#scrim').hidden = true; document.body.style.overflow=''; }
$('#drawer-close').addEventListener('click', closeDrawer);
$('#scrim').addEventListener('click', closeDrawer);
addEventListener('keydown', e=>{ if(e.key==='Escape') closeDrawer(); });

function initFilters(){
  const counts = {};
  EVENTS.forEach(e=>counts[e.type]=(counts[e.type]||0)+1);
  const chips = [['all',`全部 ${EVENTS.length}`]].concat(Object.keys(counts).sort((a,b)=>counts[b]-counts[a]).map(t=>[t,`${TYPE_META[t]?TYPE_META[t].zh:t} ${counts[t]}`]));
  $('#type-chips').innerHTML = chips.map(([t,l],i)=>`<span class="chip${i===0?' on':''}${i===0?' all':''}" data-t="${t}">${esc(l)}</span>`).join('');
  $('#type-chips').querySelectorAll('.chip').forEach(c=>c.addEventListener('click',()=>{
    state.type = c.dataset.t;
    $('#type-chips').querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));
    c.classList.add('on');
    render();
  }));
  const years = [...new Set(EVENTS.map(e=>(e.start||'????').slice(0,4)))].sort((a,b)=>b-a);
  $('#year-nav').innerHTML = years.map(y=>`<a href="#Y${y}">${y}</a>`).join('');
}

let qt;
$('#q').addEventListener('input', e=>{ clearTimeout(qt); qt=setTimeout(()=>{state.q=e.target.value; render();},180); });

fetch('./data/events.json').then(r=>r.json()).then(d=>{
  EVENTS = (d.events||[]).filter(e=>e&&e.id);
  if(!EVENTS.length){ $('#stat-line').textContent='数据为空'; return; }
  const y0=((EVENTS[EVENTS.length-1].start||EVENTS[EVENTS.length-1].end||'????')).slice(0,4), y1=((EVENTS[0].start||EVENTS[0].end||'????')).slice(0,4);
  $('#stat-line').textContent = `${EVENTS.length} 项活动 · ${y0}–${y1} · 更新 ${(d.generated_at||'').slice(5,10)}`;
  initFilters(); render();
}).catch(()=>{ $('#stat-line').textContent='数据加载失败,请刷新重试'; });
