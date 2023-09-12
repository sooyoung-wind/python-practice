import plotly
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

# https://docs.google.com/presentation/d/1DJjkdlC9mTbBAfL9tHpK-W_pRolegh0khsfDpho9EmU/edit?usp=sharing
external_stylesheets = [dbc.themes.FLATLY]  # CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# 'total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size'
#     16.99     1.01  Female     No      Sun   Dinner    2
df = plotly.data.tips()


@callback(
    Output(component_id='bar_graph', component_property='figure'),
    [Input(component_id='is_smoker', component_property='value')]
)
def update_smoker(is_smoker):
    return px.histogram(
        data_frame=df[df['smoker'] == is_smoker],
        x='day',
        y='tip',
        histfunc='avg',
        color='sex',
        barmode="group",
        category_orders=dict(day=["Thur", "Fri", "Sat", "Sun"])
    )


app.layout = dbc.Container([
    # seaborn
    # data, x, y, hue
    # plotly
    # data_frame, x, y, color
    dbc.Row([
        dbc.Col(dbc.RadioItems(id='is_smoker', options={'Yes': 'smoker', 'No': 'non smoker'}, value='No'), width=2),
        dbc.Col(dcc.Graph(id='bar_graph', figure={}), width=10)
    ]),
], style={'backgroundColor': 'yellow'}, fluid=True)

if __name__ == '__main__':
    app.run(debug=True)