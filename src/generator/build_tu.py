# -*- coding: utf-8 -*-
"""Сборка «Генератор ТУ.html»: проект (12 л.) + протокол (2 л.) на одной странице.
Вход: собранные генераторы проекта и протокола (лежат рядом), подпись, журнал из ../../Проекты и ../../Протоколы.
Запуск: python3 build_tu.py"""
import json, re, os, sys, base64, glob, hashlib, unicodedata
PUBLIC = "--public" in sys.argv          # без журнала заказчиков и без подписей — для GitHub

HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.abspath(os.path.join(HERE, "..", ".."))           # _Генератор ТУ
nfc = lambda s: unicodedata.normalize("NFC", s)

def part(path, pref):
    s = open(path, encoding="utf-8").read()
    a = s.index('<main id="sheets">') + len('<main id="sheets">'); b = s.index("</main>", a)
    main = s[a:b]
    main = re.sub(r'id="pg(\d+)"', lambda m: f'id="{pref}{m.group(1)}"', main)
    main = re.sub(r'data-p="(\d+)"', lambda m: f'data-p="{pref}{m.group(1)}"', main)
    def js(name):
        i = s.index(f"const {name} = ") + len(f"const {name} = "); j = s.index(";\n", i)
        return json.loads(s[i:j])
    dyn = js("DYN")
    for d in dyn:
        d["p"] = f"{pref}{d['p']}"; d["s"] = pref
    font = re.search(r"base64,([A-Za-z0-9+/=]+)\) format", s).group(1)
    return main, dyn, js("DEF"), font

pm, pd, pdef, font = part(os.path.join(HERE, "Генератор проекта.html"), "p")
rm, rd, rdef, _ = part(os.path.join(HERE, "Генератор протокола.html"), "r")
sign = "" if PUBLIC else "data:image/png;base64," + base64.b64encode(open(os.path.join(G, "_исходники", "протокол", "sign_usubaliev.png"), "rb").read()).decode()
if PUBLIC:
    pm = re.sub(r'<image x="288\.0" y="563\.04"[^>]*/>', "", pm)      # подпись директора на титуле
    for D in (pdef, rdef):
        for k in ("object", "addr", "customer", "order", "tu_num", "tu_date", "tp", "district"):
            if k in D: D[k] = ""

# ---------- журнал: всё, что уже выдано ----------
def iso(dmy):
    m = re.match(r"(\d\d)\.(\d\d)\.(\d{4})", dmy or "")
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""
projs = []
for f in glob.glob(os.path.join(G, "Проекты", "*.json")):
    try: projs.append(json.load(open(f, encoding="utf-8")))
    except Exception: pass
seed = []
for f in sorted(glob.glob(os.path.join(G, "Протоколы", "*.json"))):
    try: R = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    cust = R.get("customer", "")
    P = next((p for p in projs if p.get("addr") == R.get("addr") and cust in p.get("object", "")), None) \
        or next((p for p in projs if cust and cust in p.get("object", "") and p.get("len_plan") == R.get("length")), None) or {}
    obj = (P.get("object", "").replace(cust, "").strip()) or R.get("object", "")
    kw = re.match(r"[\d.,]+", P.get("power", "") or "")
    F = {"tu": P.get("tu_num", ""), "tud": iso(P.get("tu_date", "")), "org": P.get("tu_org", "ОАО НЭСК ЧуПЭС"),
         "custRaw": cust, "cust": cust, "obj": obj, "addr": P.get("addr", R.get("addr", "")),
         "dist": P.get("district", R.get("district", "")), "kw": kw.group(0) if kw else "",
         "conn": "РУ" if "РУ" in P.get("line", "") else "ВЛ", "tp": P.get("tp", ""),
         "cable": P.get("cable", R.get("cable_type", "")), "sect": re.sub(r"[()]|\s*мм²?", "", P.get("sect", R.get("sect", ""))).strip(),
         "len": P.get("len_plan", R.get("length", "")),
         "prDate": f'{R.get("year")}-{R.get("month")}-{R.get("day")}', "numK": R.get("numK", ""),
         "prObj": R.get("object", ""), "prAddr": R.get("addr", ""), "tAir": R.get("temp_air", ""), "sky": R.get("sky", ""),
         "w10": R.get("weather10", ""), "amp1": P.get("amp1", ""), "amp2": P.get("amp2", ""), "amp3": P.get("amp3", "")}
    for k in ("rA1", "rA2", "rB1", "rB2", "rC1", "rC2"): F[k] = R.get(k, "")
    hid = "s" + hashlib.md5(nfc(os.path.basename(f)).encode()).hexdigest()[:10]
    seed.append({"id": hid, "F": F, "MAN": ["cust", "prDate", "numK", "prObj", "prAddr", "len", "wx", "iso", "amp"], "saved": ""})

if PUBLIC: seed = []
tpl = open(os.path.join(HERE, "app.html"), encoding="utf-8").read()
J = lambda o: json.dumps(o, ensure_ascii=False)
out = (tpl.replace("/*FONT*/", font).replace("<!--PROJ-->", pm).replace("<!--PROT-->", rm)
          .replace("/*DYN*/", J(pd + rd)).replace("/*PDEF*/", J(pdef)).replace("/*RDEF*/", J(rdef))
          .replace("/*SIGN*/", sign).replace("/*SEED*/", J(seed)))
dst = next((a for a in sys.argv[1:] if not a.startswith("--")), os.path.join(G, "Генератор ТУ.html"))
open(dst, "w", encoding="utf-8").write(out)
print("ок:", dst, round(os.path.getsize(dst) / 1e6, 2), "МБ; dyn", len(pd), "+", len(rd), "; журнал", len(seed))
