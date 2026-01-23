---
title: "dirsearch+sqlmap"
date: 2026-01-21 19:39:43
categories:
  - ctf学习
  - 软件使用命令
tags: [dirsearch+sqlmap]
---

## dirsearch

python dirsearch.py -u "http://..." -t 1 -d 5 --full-url -R 5 -w ./ctf_high.txt

python dirsearch.py -u "http://..." -t 1 -d 5 -w ./ctf_high.txt





## sqlmap

sqlmap -u "鐩爣URL" --tamper=space2comment.py,base64encode.py --random-agent --delay 1



python sqlmap.py -u "http://..." --batch --risk=3 --level=5




sqlmap -u "http://..." --batch --risk=3 --level=5 --threads=10 --dbs --dbms=MySQL --technique=B,U,E,T,OR --tamper=between,space2plus,randomcase,htmlentitydecode,equaltolike
