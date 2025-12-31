# -*- coding: utf-8 -*-
#
##
###
####
#####

import os
from pathlib import Path
import sqlite3

script_dir = Path(__file__).parent
__bike__ = Path(script_dir, 'static', 'bike_data-demo.db') ## dev

def init_db():
    if not os.path.exists(__bike__):
        conn = sqlite3.connect(__bike__)
        c = conn.cursor()
        c.execute('''CREATE TABLE bike_data
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      day TEXT NOT NULL,
                      speed REAL NOT NULL,
                      distance REAL NOT NULL,
                      time REAL NOT NULL);''')
        conn.commit()
        conn.close()


    return True

