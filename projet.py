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

cursor.execute('''INSERT INTO vallee (id_v , nom) VALUES (1 , 'Ossau')''')
cursor.execute('''INSERT INTO vallee (id_v , nom) VALUES (2 , 'Luz')''')

cursor = connexion.cursor()
with open('Repro_IS.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    variable1_id = 1
    variable2_id = 1

    for row in reader:

        query1 = 'SELECT id_s FROM station WHERE nom="{}"'.format(
            row['Station'])
        query2 = 'SELECT id_a FROM arbre WHERE code="{}"'.format(row['code'])
        result1 = cursor.execute(query1)
        result2 = cursor.execute(query2)
        if result1.fetchone() == None:
            cursor.execute('''INSERT INTO station (id_s , nom , range , altitude) VALUES ({},"{}",{},{})'''.format(
                variable1_id, row['Station'], row['Range'], row['Altitude']))
            variable1_id = variable1_id+1

        if result2.fetchone() == None:
            if row['VH'] == "NA":
                row['VH'] = "NULL"
            if row['H'] == "NA":
                row['H'] = "NULL"
            if row['SH'] == "NA":
                row['SH'] = "NULL"
            cursor.execute('''INSERT INTO arbre (id_a , code , VH , H , SH) VALUES ({},"{}","{}","{}","{}")'''.format(variable2_id,
                                                                                                                      row['code'], row['VH'], row['H'], row['SH']))
            variable2_id = variable2_id+1
