---
title: 'dirsearch+sql慢速扫描命令'
categories:
  - 
tags: []
abbrlink: f3526173
date: 2026-03-08 15:43:44
---
# dirsearch+sql慢速扫描命令

## dirsearch

python dirsearch.py -u "http://93781c8e-cb96-40b4-89cc-615491bd3538.node5.buuoj.cn:81" -t 1 -d 5 --full-url -R 5 -w ./ctf_high.txt

python dirsearch.py -u "http://..." -t 1 -d 5 -w ./ctf_high.txt

python dirsearch.py -u http://93781c8e-cb96-40b4-89cc-615491bd3538.node5.buuoj.cn:81 -e *

python dirsearch.py -u "http://93781c8e-cb96-40b4-89cc-615491bd3538.node5.buuoj.cn:81" -t 2 --delay=0.5

dirsearch -e * -u "http://e29de8ac-3508-4880-8ca1-958ff86fdb79.node5.buuoj.cn:81" -t 1 --delay=1 --timeout=2 -x 400,403,404,500,503,429


python dirsearch.py -u http://93781c8e-cb96-40b4-89cc-615491bd3538.node5.buuoj.cn:81 -e php,bak,zip,tar.gz,txt,swp


## sqlmap

sqlmap -u "目标URL" --tamper=space2comment.py,base64encode.py --random-agent --delay 1



python sqlmap.py -u "http://..." --batch --risk=3 --level=5




sqlmap -u "http://..." --batch --risk=3 --level=5 --threads=10 --dbs --dbms=MySQL --technique=B,U,E,T,OR --tamper=between,space2plus,randomcase,htmlentitydecode,equaltolike

