# -*- coding: utf-8 -*-
"""Закрывает HTML личным кодом: AES-256-GCM, ключ из кода через PBKDF2-SHA256.
В репозиторий попадает только зашифрованный файл; код в репозиторий не пишется.
Запуск: python lock.py <открытый.html> <закрытый.html>   (код спросит или возьмёт из TU_CODE)"""
import sys, os, gzip, json, base64, getpass
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 600_000
src, dst = sys.argv[1], sys.argv[2]
code = os.environ.get("TU_CODE") or getpass.getpass("Код доступа: ")
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(code.strip().encode())
data = AESGCM(key).encrypt(iv, gzip.compress(open(src, "rb").read(), 9), None)
b64 = lambda b: base64.b64encode(b).decode()
blob = json.dumps({"s": b64(salt), "i": b64(iv), "n": ITER, "d": b64(data)})
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lock_template.html"), encoding="utf-8").read()
open(dst, "w", encoding="utf-8").write(tpl.replace("/*BLOB*/", blob))
print("закрыто:", dst, round(os.path.getsize(dst) / 1e6, 2), "МБ")
