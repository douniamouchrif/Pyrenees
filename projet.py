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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS station (
    id_s INTEGER PRIMARY KEY AUTOINCREMENT, 
    nom TEXT NOT NULL,
    range REAL,
    altitude REAL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS vallee (
    id_v INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
    );
''')


data = pd.read_csv('Repro_IS.csv', sep=';')
data.to_sql('Repro_data', connexion, if_exists='replace', index=False)
