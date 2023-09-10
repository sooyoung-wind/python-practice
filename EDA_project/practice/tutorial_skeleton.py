import plotly
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.FLATLY]  # CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# https://vincentarelbundock.github.io/Rdatasets/doc/reshape2/tips.html
# 'total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size'
#     16.99     1.01   Female    No      Sun   Dinner    2
df = plotly.data.tips()

app.layout = dbc.Container([html.H4('hello world')])

if __name__ == '__main__':
    app.run(debug=True)