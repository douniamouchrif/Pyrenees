import sqlite3
import pandas as pd
import csv

connexion = sqlite3.connect('Pyrenees.db')
cursor = connexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS vallee (
    id_v INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_v TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS station (
    id_s INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_s TEXT NOT NULL,
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pyrenees (
    id_p INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_v TEXT NOT NULL,
    nom_s TEXT NOT NULL,
    range REAL,
    altitude REAL,
    code TEXT NOT NULL,
    VH REAL,
    H REAL,
    SH REAL,
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

# table vallee
cursor.execute('INSERT INTO vallee (nom_v) VALUES ("Ossau")')
cursor.execute('INSERT INTO vallee (nom_v) VALUES ("Luz")')


def verif(value):
    if value == "NA":
        return "null"
    else:
        return value


cursor = connexion.cursor()
with open('Repro_IS.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    for row in reader:

        # table station
        query = 'SELECT id_s FROM station WHERE nom_s="{}"'.format(
            row['Station'])
        result = cursor.execute(query)
        if result.fetchone() == None:
            cle = cursor.execute('SELECT id_v FROM vallee WHERE nom_v="{}"'.format(
                row['Valley']))
            cle_id = cle.fetchone()
            query = 'INSERT INTO station (nom_s , range , altitude, vallee_id) VALUES ("{}",{},{},{})'.format(
                verif(row['Station']), verif(row['Range']), verif(row['Altitude']), cle_id[0])
            cursor.execute(query)

        # table arbre
        query = 'SELECT id_a FROM arbre WHERE code="{}"'.format(row['code'])
        result = cursor.execute(query)
        if result.fetchone() == None:
            cle = cursor.execute('SELECT id_s FROM station WHERE nom_s="{}"'.format(
                row['Station']))
            cle_id = cle.fetchone()
            query = 'INSERT INTO arbre (code , VH , H , SH, station_id) VALUES ("{}","{}","{}","{}",{})'.format(
                verif(row['code']), verif(row['VH']), verif(row['H']), verif(row['SH']), cle_id[0])
            cursor.execute(query)

        # table recolte
        cle = cursor.execute('SELECT id_a FROM arbre WHERE code="{}"'.format(
            row['code']))
        cle_id = cle.fetchone()
        query = 'INSERT INTO recolte (harv_num, DD, harv, Year, Date, Mtot, Ntot, Ntot1, oneacorn, tot_Germ, M_Germ, N_Germ, rate_Germ, arbre_id) VALUES("{}", "{}", "{}", {}, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}",{})'.format(
            verif(row['harv_num']), verif(row['DD']), verif(row['harv']), verif(row['Year']), verif(row[
                'Date']), verif(row['Mtot']), verif(row['Ntot']), verif(row['Ntot1']), verif(row['oneacorn']), verif(row['tot_Germ']),
            verif(row['M_Germ']), verif(row['N_Germ']), verif(row['rate_Germ']), cle_id[0])
        cursor.execute(query)

        # table pyrenees
        query = 'INSERT INTO pyrenees (nom_v, nom_s, range, altitude, code, VH, H, SH, harv_num, DD, harv, Year, Date, Mtot, Ntot, Ntot1, oneacorn, tot_Germ, M_Germ, N_Germ, rate_Germ) VALUES("{}","{}",{},{},"{}","{}","{}","{}","{}","{}","{}",{},"{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(
            verif(row['Valley']), verif(row['Station']), verif(row['Range']), verif(
                row['Altitude']), verif(row['code']), verif(row['VH']), verif(row['H']), verif(row['SH']),
            verif(row['harv_num']), verif(row['DD']), verif(row['harv']), verif(row['Year']), verif(
                row['Date']), verif(row['Mtot']), verif(row['Ntot']), verif(row['Ntot1']),
            verif(row['oneacorn']), verif(row['tot_Germ']), verif(row['M_Germ']), verif(row['N_Germ']), verif(row['rate_Germ']))
        cursor.execute(query)

connexion.commit()
connexion.close()
