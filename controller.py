import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import model.data
import view.GUI


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
        dropdown = view.GUI.build_dropdown_menu(model.data.get_year())
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
        dropdown = view.GUI.build_dropdown_menu(model.data.get_year())
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


@app.callback(Output(component_id='pie_chart', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_values):
    if dropdown_values == None:
        raise PreventUpdate
    dataa = model.data.prepare_data_pie_chart(dropdown_values)
    year = list(dropdown_values)
    return view.GUI.build_graph_pie_chart(dataa, year)


@app.callback(Output(component_id='scatter', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_values):
    if dropdown_values == None:
        raise PreventUpdate
    df = model.data.prepare_data_scatter(dropdown_values)
    year = list(dropdown_values)
    return view.GUI.build_scatter(df, year)


if __name__ == '__main__':
    app.run_server(debug=True)
