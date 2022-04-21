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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS arbre_station ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    arbre_id INT NOT NULL,
    station_id INT NOT NULL,
    FOREIGN KEY (arbre_id) REFERENCES arbre (id_a),
    FOREIGN KEY (station_id) REFERENCES station (id_s)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS arbre_recolte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    arbre_id INT NOT NULL, 
    recolte_id INT NOT NULL, 
    FOREIGN KEY (arbre_id) REFERENCES arbre (id_a), 
    FOREIGN KEY (recolte_id) REFERENCES recolte (id_r)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS station_vallee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INT NOT NULL, 
    vallee_id INT NOT NULL, 
    FOREIGN KEY (station_id) REFERENCES station (id_s), 
    FOREIGN KEY (vallee_id) REFERENCES vallee (id_v)
    );
''')

data = pd.read_csv('Repro_IS.csv', sep=';')
data.to_sql('Repro_data', con, if_exists='replace', index=False)
