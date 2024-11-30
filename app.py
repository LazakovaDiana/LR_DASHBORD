import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Загрузка данных из CSV файла
# Предположим, что файл называется "website_visits.csv"
df = pd.read_csv('website_visits.csv')

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Основная структура дашборда
app.layout = html.Div(children=[
    html.H1(children='Дашборд посещаемости веб-сайта'),

    # График временного ряда
    dcc.Graph(id='time-series-graph'),

    # Круговая диаграмма
    dcc.Graph(id='pie-chart'),

    # Гистограмма
    dcc.Graph(id='histogram'),

    # Таблица с данными
    dcc.Graph(id='data-table'),

    # Выпадающий список для выбора периода анализа
    dcc.Dropdown(
        id='period-dropdown',
        options=[
            {'label': 'Месяц', 'value': 'month'},
            {'label': 'Квартал', 'value': 'quarter'},
            {'label': 'Год', 'value': 'year'}
        ],
        value='month'
    ),

    # Индикаторы для отображения текущих значений показателей
    html.Div(id='current-indicators')
])

# Обновление графиков и индикаторов на основе выбранного периода
@app.callback(
    [Output('time-series-graph', 'figure'),
     Output('pie-chart', 'figure'),
     Output('histogram', 'figure'),
     Output('data-table', 'figure'),
     Output('current-indicators', 'children')],
    [Input('period-dropdown', 'value')]
)
def update_graphs(selected_period):
    # Фильтрация данных в зависимости от выбранного периода
    if selected_period == 'month':
        filtered_df = df[df['date'].dt.month == pd.Timestamp.now().month]
    elif selected_period == 'quarter':
        filtered_df = df[df['date'].dt.quarter == pd.Timestamp.now().quarter]
    else:
        filtered_df = df[df['date'].dt.year == pd.Timestamp.now().year]

    # График временного ряда
    time_series_fig = px.line(filtered_df, x='date', y='visits', title='Посещения по времени')

    # Круговая диаграмма
    pie_fig = px.pie(filtered_df, names='category', values='visits', title='Структура посещений по категориям')

    # Гистограмма
    histogram_fig = px.histogram(filtered_df, x='visits', nbins=20, title='Гистограмма посещений')

    # Таблица с данными (можно использовать Plotly Dash DataTable)
    data_table_fig = {
        'data': [{
            'type': 'table',
            'header': {
                'values': ['Дата', 'Посещения', 'Категория'],
                'fill': {'color': '#C2D4FF'},
                'align': ['left'] * 3,
            },
            'cells': {
                'values': [filtered_df['date'], filtered_df['visits'], filtered_df['category']],
                'fill': {'color': '#F5F8FF'},
                'align': ['left'] * 3,
            }
        }]
    }

    # Индикаторы текущих значений
    current_visits = filtered_df['visits'].sum()
    current_indicators = [
        html.Div(f'Текущие посещения: {current_visits}', style={'fontSize': 20}),
        html.Div(f'Количество уникальных категорий: {filtered_df["category"].nunique()}', style={'fontSize': 20}),
    ]

    return time_series_fig, pie_fig, histogram_fig, data_table_fig, current_indicators

if __name__ == '__main__':
    app.run_server(debug=True)