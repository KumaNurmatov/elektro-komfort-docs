# -*- coding: utf-8 -*-
"""Скриншоты для help.html: публичная сборка генератора (без журнала заказчиков и подписей)
+ выдуманные данные + пронумерованные пометки поверх. Headless Chrome, retina.
Запуск: python3 src/help/shots.py <публичная сборка Генератор ТУ.html>"""
import sys, os, json, subprocess, shutil, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "help")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
os.makedirs(OUT, exist_ok=True)
TMP = tempfile.mkdtemp(prefix="tu-help-")

def entry(i, tu, tud, raw, cust, addr, num, pr):
    return {"id": f"demo{i}", "MAN": ["cust","prDate","numK","prObj","prAddr","len","wx","iso","amp"], "saved": "",
            "F": {"tu": tu, "tud": tud, "org": "ОАО НЭСК ЧуПЭС", "custRaw": raw, "cust": cust, "obj": "Жилой дом", "addr": addr,
                  "dist": "Панфиловский район", "kw": "10", "conn": "ВЛ", "tp": "ф-2 опора №7 ТП-П000", "cable": "АВВГ", "sect": "4х16",
                  "len": "27", "prDate": pr, "numK": num, "prObj": "Жилой дом", "prAddr": addr, "tAir": "16", "sky": "ясно", "w10": "21",
                  "rA1": "801", "rA2": "803", "rB1": "795", "rB2": "795", "rC1": "788", "rC2": "791", "amp1": "25", "amp2": "25", "amp3": "25"}}
JOURNAL = [entry(1, "565/40б", "2026-10-20", "Петрова С.А.", "Петров С.А.", "с. Примерное, ул. Садовая 12", "100", "2026-10-21"),
           entry(2, "565/41б", "2026-10-20", "Сидоровой Г.К.", "Сидорова Г.К.", "с. Примерное, ул. Луговая 3", "98", "2026-10-21"),
           entry(3, "565/38б", "2026-10-17", "Касымова Б.Т.", "Касымов Б.Т.", "с. Новое, ул. Мира 40", "96", "2026-10-18")]
FORM = {"tu": "565/45б", "tud": "2026-11-02", "org": "", "custRaw": "Иванова А.Б.", "cust": "", "obj": "Жилой дом",
        "addr": "с. Примерное, ул. Центральная 1", "dist": "Панфиловский район", "kw": "10", "conn": "ВЛ", "tp": "ф-1 опора №5 ТП-П000",
        "cable": "АВВГ", "sect": "4х16", "len": "", "prDate": "", "numK": "", "prObj": "", "prAddr": "", "tAir": "14", "sky": "ясно", "w10": "19",
        "rA1": "", "rA2": "", "rB1": "", "rB2": "", "rC1": "", "rC2": "", "amp1": "", "amp2": "", "amp3": ""}
DUP = dict(FORM, tu="565/40б", custRaw="Петрова С.А.", addr="с. Примерное, ул. Садовая 12")

PRE = """<script>(function(){const h=location.hash.slice(1);localStorage.clear();
localStorage.setItem('tu_journal',JSON.stringify(%s));
localStorage.setItem('tu_form',JSON.stringify({F:h==='dup'?%s:%s,MAN:[],CUR:null}));})();</script>""" % (
    json.dumps(JOURNAL, ensure_ascii=False), json.dumps(DUP, ensure_ascii=False), json.dumps(FORM, ensure_ascii=False))

POST = r"""<style>.mk{position:absolute;border:3px solid #e11d48;border-radius:9px;pointer-events:none;z-index:9999;box-shadow:0 0 0 3px rgba(255,255,255,.7)}
.mk b{position:absolute;left:-15px;top:-15px;width:28px;height:28px;border-radius:50%;background:#e11d48;color:#fff;font:700 15px/28px -apple-system,Arial;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.4)}</style>
<script>
function mk(sel,n,pad=4,pos){const e=typeof sel==='string'?document.querySelector(sel):sel;if(!e)return;
 const host=/^(INPUT|SELECT|TEXTAREA|BUTTON)$/.test(e.tagName)?e.parentElement:e;   // пометка — дочерний элемент, едет вместе с ним
 if(getComputedStyle(host).position==='static')host.style.position='relative';
 const d=document.createElement('div');d.className='mk';d.style.position='absolute';
 if(host===e){d.style.inset=(-pad)+'px';}else{d.style.left=(e.offsetLeft-pad)+'px';d.style.top=(e.offsetTop-pad)+'px';d.style.width=(e.offsetWidth+2*pad)+'px';d.style.height=(e.offsetHeight+2*pad)+'px';}
 d.innerHTML='<b>'+n+'</b>';const bb=d.querySelector('b');if(pos&&pos.includes('r')){bb.style.left='auto';bb.style.right='-15px';}if(pos&&pos.includes('b')){bb.style.top='auto';bb.style.bottom='-15px';}host.appendChild(d);}
const lab=k=>document.querySelector('[data-f='+k+']').closest('label');
const fs=t=>[...document.querySelectorAll('fieldset')].find(f=>f.querySelector('legend').textContent.includes(t));
setTimeout(()=>{const h=location.hash.slice(1);
 const W='Погода 03.11.2026, Панфиловский район: 14 °C днём, ясно, макс. за 10 дн. 19 °C (Open-Meteo)';try{wxStatus(W);}catch(_){}
 if(h==='overview'){mk('#tabs',1);mk(fs('Из технических'),2,3);mk(lab('cust'),3,3);mk('#bar .seg',4,4,'b');mk('#pdfP',5,3,'b');mk('#pdfR',5,3,'b');mk('#prAll',6,3,'br');mk('#zp',7,3,'br');mk('#pfoot',8,2);}
 if(h==='protocol'){document.querySelector('[data-view=prot]').click();const f=fs('Протокол');document.getElementById('pbody').scrollTop=f.offsetTop-10;
  setTimeout(()=>{mk(lab('prDate'),1,3);mk(lab('numK'),2,3);mk('#numHint',2,2);mk('#wxStatus',3,2);mk(document.querySelector('.isogrid'),4,4);mk(lab('len'),5,3);},150);}
 if(h==='dup'){mk('#notes .note',1,3);}
 if(h==='journal'){showTab('jour');setTimeout(()=>{mk('#jsearch',1,3);mk(document.querySelector('.jr'),2,3);mk('.jtools',3,3);mk('[data-tab=jour]',4,2);},100);}
 if(h==='consts'){const d=document.getElementById('constBox');d.open=true;setTimeout(()=>{d.scrollIntoView({block:'start'});document.getElementById('pbody').scrollTop-=12;setTimeout(()=>{mk(d.querySelector('summary'),1,2);mk(document.querySelector('[data-c=org]').closest('label'),2,3);},80);},80);}
 if(h==='m-form'){mk('#mnav',1,0);mk('#pfoot',2,0);mk(lab('cust'),3,3);}
 if(h==='m-sheets'){setM('sheets');setTimeout(()=>{mk('#zp',1,3,'b');mk('#bar',2,0,'r');},200);}
 if(h==='m-jour'){setM('jour');setTimeout(()=>{mk(document.querySelector('.jr'),1,3);},100);}
},900);
</script>"""

src = open(sys.argv[1], encoding="utf-8").read()
src = src.replace("<style>", PRE + "\n<style>", 1).replace("</body>", POST + "\n</body>")
page = os.path.join(TMP, "shot.html"); open(page, "w", encoding="utf-8").write(src)

lock = open(os.path.join(REPO, "src", "lock_template.html"), encoding="utf-8").read().replace("/*BLOB*/", '{"s":"","i":"","n":1,"d":""}')
lock = lock.replace("</body>", POST.replace("setTimeout(()=>{const h", "setTimeout(()=>{if(location.hash==='#login'){document.getElementById('c').value='•••••••••••••';mk('#c',1,3);mk('#r',2,6);mk('#b',3,3);}const h") + "</body>")
lockp = os.path.join(TMP, "lock.html"); open(lockp, "w", encoding="utf-8").write(lock)

SHOTS = [("login", lockp, (390, 700)), ("overview", page, (1440, 900)), ("protocol", page, (1440, 900)), ("dup", page, (1440, 900)),
         ("journal", page, (1440, 900)), ("consts", page, (1440, 900)),
         ("m-form", page, (390, 844)), ("m-sheets", page, (390, 844)), ("m-jour", page, (390, 844))]
prof = os.path.join(TMP, "prof")
from PIL import Image
for name, f, (w, h) in SHOTS:
    dst = os.path.join(OUT, name + ".png"); url = "file://" + f + "#" + name; win = w
    if w < 500:      # headless не даёт окно уже 500 px — телефон кладём в рамку
        fr = os.path.join(TMP, f"frame-{name}.html")
        open(fr, "w", encoding="utf-8").write(f'<!doctype html><body style="margin:0;background:#fff"><iframe src="{url}" style="border:0;width:{w}px;height:{h}px;display:block"></iframe></body>')
        url, win = "file://" + fr, 520
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-first-run", f"--user-data-dir={prof}",
                    "--allow-file-access-from-files", f"--window-size={win},{h}", "--force-device-scale-factor=2", "--virtual-time-budget=8000",
                    f"--screenshot={dst}", url], capture_output=True, timeout=120)
    if win != w and os.path.exists(dst):
        Image.open(dst).crop((0, 0, w * 2, h * 2)).save(dst)
    print(name, os.path.exists(dst) and os.path.getsize(dst))
shutil.rmtree(TMP, ignore_errors=True)
