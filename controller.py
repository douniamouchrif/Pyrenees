import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import model.data
import view.GUI

import plotly.express as px
import pandas as pd


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

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
                dbc.NavLink("Tableur",
                            href="/table", active="exact"),
                dbc.NavLink("Pie-Chart",
                            href="/pie_chart", active="exact"),
                dbc.NavLink("Scatter-Chart",
                            href="/scatter_chart", active="exact"),
                dbc.NavLink("Animation",
                            href="/animation", active="exact"),
                dbc.NavLink("Box-Plot",
                            href="/box_plot", active="exact"),
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
    if pathname == "/table":
        return [
            html.H1('Données forêt pyrénnées (tableur)', id='table_view',
                    style={'textAlign': 'left'}),
            html.Hr(style={'width': '75%', 'align': 'center'}),
            html.Div(id='data_table', children=view.GUI.data_table(
                model.data.get_data_table()))
        ]

    elif pathname == "/pie_chart":
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

    elif pathname == "/box_plot":
        dropdown = view.GUI.build_dropdown_multi(model.data.get_year()),
        graph = dcc.Graph(id="box"),
        return [
            html.H1('Observation par Box-Plot',
                    style={'textAlign': 'center'}),
            html.Div([
                html.P("Select a parametre :"),
                dcc.RadioItems(
                    id='y-axis',
                    options=[
                        {'label': 'Hauteur', 'value': 'H'},
                        {'label': 'SH', 'value': 'SH'},
                        {'label': 'Volume du Houpier', 'value': 'VH'}
                    ],
                    value='H',
                ),
                html.P("Year :"),
                dropdown,
                graph
            ])
        ]

# PIE CHART


@app.callback(Output(component_id='pie_chart', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_values):
    if dropdown_values == None:
        dataa = model.data.prepare_data_pie_chart([2014])
        return view.GUI.build_graph_pie_chart(dataa, [2014])
    dataa = model.data.prepare_data_pie_chart(dropdown_values)
    year = list(dropdown_values)
    return view.GUI.build_graph_pie_chart(dataa, year)

# SCATTER


@app.callback(Output(component_id='scatter', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_values):
    if dropdown_values == None:
        df = model.data.prepare_data_scatter([2015])
        return view.GUI.build_scatter(df, [2015])
    df = model.data.prepare_data_scatter(dropdown_values)
    year = list(dropdown_values)
    return view.GUI.build_scatter(df, year)

# ANIMATION


@app.callback(
    Output('anime', 'figure'),
    Input('dropdown', 'value'))
def update_graph(value_vallee):
    df = model.data.update_scatter(value_vallee)
    return view.GUI.build_new_scatter(df)


@app.callback(
    Output('x-time-series', 'figure'),
    Input('anime', 'hoverData'))
def update_y_timeseries(hoverData):
    print(hoverData)
    if hoverData is None:
        new = model.data.update_hoverData('Josbaig')
        return view.GUI.create_time_series(new, "H")
    else:
        station_name = hoverData['points'][0]['hovertext']
        new = model.data.update_hoverData(station_name)
        return view.GUI.create_time_series(new, "H")


@app.callback(
    Output('y-time-series', 'figure'),
    Input('anime', 'hoverData'))
def update_x_timeseries(hoverData):
    print(hoverData)
    if hoverData is None:
        new = model.data.update_hoverData('Josbaig')
        return view.GUI.create_time_series(new, "VH")
    else:
        station_name = hoverData['points'][0]['hovertext']
        new = model.data.update_hoverData(station_name)
        return view.GUI.create_time_series(new, "VH")

# BOX PLOT


@app.callback(Output(component_id='box', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')],
              Input("y-axis", "value"))
def generate_chart(dropdown_values, y):
    if dropdown_values == None:
        raise PreventUpdate
    dataa = model.data.prepare_data_box_plot(dropdown_values)
    year = list(dropdown_values)
    return view.GUI.build_graph_box_plot(dataa, year, y)


if __name__ == '__main__':
    app.run_server(debug=True)
