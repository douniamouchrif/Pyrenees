import sqlite3
import pandas as pd

connexion = sqlite3.connect('Pyrenees.db')
cursor = connexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS arbre (
    id_a INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    VH REAL,
    H REAL,
    SH REAL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS récolte (
    id_r INTEGER PRIMARY KEY AUTOINCREMENT,
    ID TEXT NOT NULL,
    harv_num REAL,
    DD REAL,
    harv REAL,
    Year INTEGER,
    Date DATETIME,
    Mtot REAL,
    Ntot REAL,
    Ntot1 REAL,
    oneacorn REAL,
    tot_Germ REAL,
    M_Germ REAL, 
    N_Germ REAL, 
    rate_Germ REAL
    );
''')