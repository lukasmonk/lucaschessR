import os
import sys
import sqlite3
import time
from imp import reload

reload(sys)
sys.setdefaultencoding("latin-1")
sys.path.insert(0, os.curdir)

current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
if current_dir:
    os.chdir(current_dir)

from Code import Util

sys.path.append(os.path.join(current_dir, "Code"))

import Code.Traducir as Traducir
Traducir.install()

key = sys.argv[1]
file_variables = sys.argv[2]
file_destino = sys.argv[3]

db = Util.DicSQL(file_variables)

dic = {}
for k in db.keys():
    if k.startswith(key):
        try:
            dato = db[k]
            dic[k] = dato
        except:
            pass

with open(file_destino, "wt") as q:
    q.write(str(dic))

db.close()
