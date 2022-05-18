from dash import dcc
import plotly.express as px


def build_dropdown_multi(item_list):
    options = [{"label": x, "value": x} for x in item_list]
    return dcc.Dropdown(id='dropdown',
                        options=options,
                        multi=True)


def build_dropdown_select(item_list):
    options = [{"label": x, "value": x} for x in item_list]
    return dcc.Dropdown(id='dropdown',
                        options=options,
                        value=item_list[0])


def build_graph_pie_chart(dataa, year):
    graphh = px.sunburst(dataa, path=['nom_v', 'nom_s', 'code'], values='Ntot', color='nom_s',
                         title='Evolution des récoltes – Year {}'.format(year))
    return graphh


def build_scatter(df, year):
    fig = px.scatter(df, x="SH", y="Ntot", animation_group="Ntot", animation_frame="Year",
                     size="rate_Germ", color="nom_s", hover_name="nom_v", log_x=True, log_y=True,
                     trendline="ols", trendline_scope="overall", trendline_color_override="black",
                     title='Evolution des récoltes – Year {}'.format(year))
    return fig


def build_new_scatter(df):
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


def create_time_series(dff, k):

    fig = px.scatter(dff, x='Year', y=k)

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left')

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


def build_graph_box_plot(dataa, year, y):
    fig = px.box(dataa, x='nom_s', y=y, color='nom_s',
                 title='Observations – Year {}'.format(year))
    return fig
