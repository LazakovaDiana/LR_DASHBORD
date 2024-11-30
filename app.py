import dash
from dash import dcc, html

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Дашборд посещаемости веб-сайта'),
    dcc.Graph(id='example-graph'),
    dcc.Dropdown(
        id='period-dropdown',
        options=[
            {'label': 'Месяц', 'value': 'month'},
            {'label': 'Квартал', 'value': 'quarter'},
            {'label': 'Год', 'value': 'year'}
        ],
        value='month'
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)