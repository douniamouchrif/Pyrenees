import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import model.data
import view.GUI

import plotly.express as px
import sqlite3
import pandas as pd


app = dash.Dash()

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("Projet", className="display-4"),
        html.H2("ABARKAN & MOUCHRIF"),
        html.Hr(),
        html.P(
            "Forêt Pyrénnées", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Pie-Chart",
                            href="/pie_chart", active="exact"),
                dbc.NavLink("Scatter-Chart",
                            href="/scatter_chart", active="exact"),
                dbc.NavLink("Animation",
                            href="/animation", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/pie_chart":
        dropdown = view.GUI.build_dropdown_multi(model.data.get_year())
        graph = dcc.Graph(id='pie_chart')
        return [
            html.H1(id='H1', children='Récoltes par années', style={'textAlign': 'center',
                                                                    'marginTop': 40, 'marginBottom': 40}),
            html.Div([
                html.P("Year :"),
                dropdown,
                html.Hr(),
                graph
            ])
        ]

    elif pathname == "/scatter_chart":
        dropdown = view.GUI.build_dropdown_multi(model.data.get_year())
        graph = dcc.Graph(id='scatter')
        return [
            html.H1('Visualisation des données par Scatter-Chart',
                    style={'textAlign': 'center'}),
            html.Div([
                html.P("Year :"),
                dropdown,
                html.Hr(),
                graph
            ])
        ]

    elif pathname == "/animation":
        dropdown = view.GUI.build_dropdown_select(model.data.get_vallee())
        graph = dcc.Graph(id='anime')
        graph1 = dcc.Graph(id='x-time-series')
        graph2 = dcc.Graph(id='y-time-series')
        return [
            html.H1('Animation de données',
                    style={'textAlign': 'center'}),
            html.Div([
                html.P("Vallée :"),
                dropdown,
                html.Hr(),
                graph,

            ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

            html.Div([
                graph1,
                graph2
            ], style={'display': 'block', 'width': '49%'})
        ]

# PIE CHART


@app.callback(Output(component_id='pie_chart', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_values):
    if dropdown_values == None:
        raise PreventUpdate
    dataa = model.data.prepare_data_pie_chart(dropdown_values)
    year = list(dropdown_values)
    return view.GUI.build_graph_pie_chart(dataa, year)

# SCATTER


@app.callback(Output(component_id='scatter', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_values):
    if dropdown_values == None:
        raise PreventUpdate
    df = model.data.prepare_data_scatter(dropdown_values)
    year = list(dropdown_values)
    return view.GUI.build_scatter(df, year)

# ANIMATION


@app.callback(
    Output('anime', 'figure'),
    Input('dropdown', 'value'))
def update_graph(value_vallee):
    connexion = sqlite3.connect('Pyrenees.db')
    query = 'SELECT pyrenees.H , pyrenees.VH , pyrenees.Year , pyrenees.nom_s , pyrenees.nom_v FROM pyrenees WHERE pyrenees.nom_v = "{}"'.format(
        value_vallee)
    df = pd.read_sql(query, connexion)
    fig = px.scatter(df, x='H',
                     y='VH',
                     hover_name="nom_s"
                     )

    fig.update_xaxes(title="Hauteur de l'arbre ",
                     type='linear')

    fig.update_yaxes(title="Volume de houppier",
                     type='linear')

    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


@app.callback(
    Output('x-time-series', 'figure'),
    Input('anime', 'hoverData'))
def update_y_timeseries(hoverData):
    print(hoverData)
    connexion = sqlite3.connect('Pyrenees.db')
    if hoverData is None:
        query = 'SELECT * FROM pyrenees WHERE nom_s = "{}"'.format('Josbaig')
        df = pd.read_sql(query, connexion)
        return view.GUI.create_time_series(df, "H")
    else:
        station_name = hoverData['points'][0]['hovertext']
        query = 'SELECT * FROM pyrenees WHERE nom_s = "{}"'.format(
            station_name)
        df = pd.read_sql(query, connexion)
        return view.GUI.create_time_series(df, "H")


@app.callback(
    Output('y-time-series', 'figure'),
    Input('anime', 'hoverData'))
def update_x_timeseries(hoverData):
    print(hoverData)
    connexion = sqlite3.connect('Pyrenees.db')
    if hoverData is None:
        query = 'SELECT * FROM pyrenees WHERE nom_s = "{}"'.format('Josbaig')
        df = pd.read_sql(query, connexion)
        return view.GUI.create_time_series(df, "VH")
    else:
        station_name = hoverData['points'][0]['hovertext']
        query = 'SELECT * FROM pyrenees WHERE nom_s = "{}"'.format(
            station_name)
        df = pd.read_sql(query, connexion)
        return view.GUI.create_time_series(df, "VH")


if __name__ == '__main__':
    app.run_server(debug=True)
