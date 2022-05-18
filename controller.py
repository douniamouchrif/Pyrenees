import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import model.data
import view.GUI


app = dash.Dash()

app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='Récoltes par années', style={'textAlign': 'center',
                                                            'marginTop': 40, 'marginBottom': 40}),
    html.P("Year :"),
    view.GUI.build_dropdown_menu(model.data.get_year()),
    html.Hr(),
    dcc.Graph(id='pie_chart')
]
)


@app.callback(Output(component_id='pie_chart', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(dropdown_values):
    if dropdown_values == None:
        raise PreventUpdate
    dataa = model.data.prepare_data_(dropdown_values)
    year = list(dropdown_values)
    return view.GUI.build_graph_pie_chart(dataa, year)


if __name__ == '__main__':
    app.run_server(debug=True)
