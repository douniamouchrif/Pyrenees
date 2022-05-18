from dash.exceptions import PreventUpdate
import sqlite3
import pandas as pd


def get_year():
    connexion = sqlite3.connect('Pyrenees.db')
    return [v[0] for v in pd.read_sql('SELECT DISTINCT Year FROM recolte', connexion).values]


def prepare_data_pie_chart(year_list):
    if year_list == None:
        raise PreventUpdate
    else:
        connexion = sqlite3.connect('Pyrenees.db')
        if len(year_list) == 1:
            year = year_list[0]
            query = "SELECT arbre.code, recolte.Ntot, station.nom_s, vallee.nom_v FROM arbre JOIN recolte ON arbre.id_a=recolte.arbre_id JOIN station ON station.id_s=arbre.station_id JOIN vallee ON vallee.id_v=station.vallee_id WHERE recolte.Ntot != 'null' AND recolte.year={}".format(
                year)

        else:
            query = "SELECT arbre.code, recolte.Ntot, station.nom_s, vallee.nom_v FROM arbre JOIN recolte ON arbre.id_a=recolte.arbre_id JOIN station ON station.id_s=arbre.station_id JOIN vallee ON vallee.id_v=station.vallee_id WHERE recolte.Ntot != 'null' AND recolte.year IN {}".format(
                tuple(year_list))

        df = pd.read_sql(query, connexion)
        return df


def prepare_data_scatter(year_list):
    if year_list == None:
        raise PreventUpdate
    else:
        connexion = sqlite3.connect('Pyrenees.db')
        if len(year_list) == 1:
            year = year_list[0]
            query = "SELECT SH, Year, Ntot, nom_v, nom_s, rate_Germ FROM pyrenees WHERE rate_Germ != 'null' AND Year={}".format(
                year)
        else:
            query = "SELECT SH, Year, Ntot, nom_v, nom_s, rate_Germ FROM pyrenees WHERE rate_Germ != 'null' AND Year IN {}".format(
                tuple(year_list))

        data = pd.read_sql(query, connexion)
        return data
