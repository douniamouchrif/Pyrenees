from dash import dcc
import plotly.express as px


def build_dropdown_menu(item_list):
    options = [{"label": x, "value": x} for x in item_list]
    return dcc.Dropdown(id='dropdown',
                        options=options,
                        multi=True)


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
