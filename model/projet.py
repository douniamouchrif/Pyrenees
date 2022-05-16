import sqlite3
import pandas as pd
import csv

connexion = sqlite3.connect('Pyrenees.db')
cursor = connexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS vallee (
    id_v INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS station (
    id_s INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    range REAL,
    altitude REAL,
    vallee_id INT REFERENCES vallee(id_v)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS arbre (
    id_a INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    VH REAL,
    H REAL,
    SH REAL,
    station_id INT REFERENCES station(id_s)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS recolte (
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
    rate_Germ REAL,
    arbre_id INT REFERENCES arbre(id_a)
    );
''')

cursor.execute('INSERT INTO vallee (nom) VALUES ("Ossau")')
cursor.execute('INSERT INTO vallee (nom) VALUES ("Luz")')


def verif(value):
    if value == "NA":
        return "null"
    else:
        return value


cursor = connexion.cursor()
with open('Repro_IS.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    for row in reader:

        query = 'SELECT id_s FROM station WHERE nom="{}"'.format(
            row['Station'])
        result = cursor.execute(query)
        if result.fetchone() == None:
            query = 'INSERT INTO station (nom , range , altitude) VALUES ("{}",{},{})'.format(
                verif(row['Station']), verif(row['Range']), verif(row['Altitude']))
            cursor.execute(query)

        query = 'SELECT id_a FROM arbre WHERE code="{}"'.format(row['code'])
        result = cursor.execute(query)
        if result.fetchone() == None:
            query = 'INSERT INTO arbre (code , VH , H , SH) VALUES ("{}","{}","{}","{}")'.format(
                verif(row['code']), verif(row['VH']), verif(row['H']), verif(row['SH']))
            cursor.execute(query)

        query = 'INSERT INTO recolte (harv_num, DD, harv, Year, Date, Mtot, Ntot, Ntot1, oneacorn, tot_Germ, M_Germ, N_Germ, rate_Germ) VALUES("{}", "{}", "{}", {}, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
            verif(row['harv_num']), verif(row['DD']), verif(row['harv']), verif(row['Year']), verif(row[
                'Date']), verif(row['Mtot']), verif(row['Ntot']), verif(row['Ntot1']), verif(row['oneacorn']), verif(row['tot_Germ']),
            verif(row['M_Germ']), verif(row['N_Germ']), verif(row['rate_Germ']))
        cursor.execute(query)


connexion.commit()
connexion.close()
