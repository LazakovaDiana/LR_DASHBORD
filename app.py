import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Загрузка данных из CSV файла
df = pd.read_csv('website_visits.csv')
df['date'] = pd.to_datetime(df['date'])  # Преобразование столбца даты в формат datetime

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

    # Таблица с данными (можно использовать Plotly Dash DataTable)
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


# Функция фильтрации данных в зависимости от выбранного периода
def filter_data(selected_period):
    if selected_period == 'month':
        return df[df['date'].dt.month == pd.Timestamp.now().month]
    elif selected_period == 'quarter':
        return df[df['date'].dt.quarter == pd.Timestamp.now().quarter]
    else:
        return df[df['date'].dt.year == pd.Timestamp.now().year]


# Функция для создания графика временного ряда
def create_time_series_figure(filtered_df):
    return px.line(filtered_df, x='date', y='visits', title='Посещения по времени')


# Функция для создания круговой диаграммы
def create_pie_chart(filtered_df):
    return px.pie(filtered_df, names='category', values='visits', title='Структура посещений по категориям')


# Функция для создания гистограммы
def create_histogram(filtered_df):
    return px.histogram(filtered_df, x='visits', nbins=20, title='Гистограмма посещений')


# Функция для создания таблицы с данными
def create_data_table(filtered_df):
    return {
        'data': [{
            'type': 'table',
            'header': {
                'values': ['Дата', 'Посещения', 'Уникальные посетители', 'Просмотры страниц', 'Процент отказов',
                           'Категория'],
                'fill': {'color': '#C2D4FF'},
                'align': ['left'] * 6,
            },
            'cells': {
                'values': [filtered_df['date'].dt.strftime('%Y-%m-%d'),
                           filtered_df['visits'],
                           filtered_df['unique_visitors'],
                           filtered_df['page_views'],
                           filtered_df['bounce_rate'],
                           filtered_df['category']],
                'fill': {'color': '#F5F8FF'},
                'align': ['left'] * 6,
            }
        }]
    }


# Функция для генерации индикаторов текущих значений
def generate_current_indicators(filtered_df):
    current_visits = filtered_df['visits'].sum()
    unique_visitors = filtered_df['unique_visitors'].sum()

    return [
        html.Div(f'Текущие посещения: {current_visits}', style={'fontSize': 20}),
        html.Div(f'Количество уникальных посетителей: {unique_visitors}', style={'fontSize': 20}),
        html.Div(f'Общее количество просмотров страниц: {filtered_df["page_views"].sum()}', style={'fontSize': 20}),
        html.Div(f'Средний процент отказов: {filtered_df["bounce_rate"].mean():.2f}%', style={'fontSize': 20}),
    ]


# Обновление графиков и индикаторов на основе выбранного периода
@app.callback(
    [Output('time-series-graph', 'figure'),
     Output('pie-chart', 'figure'),
     Output('histogram', 'figure'),
     Output('data-table', 'figure'),
     Output('current-indicators', 'children')],
    [Input('period-dropdown', 'value')],
    prevent_initial_call=True
)
def update_graphs(selected_period):
    filtered_df = filter_data(selected_period)

    time_series_fig = create_time_series_figure(filtered_df)
    pie_fig = create_pie_chart(filtered_df)
    histogram_fig = create_histogram(filtered_df)
    data_table_fig = create_data_table(filtered_df)
    current_indicators = generate_current_indicators(filtered_df)

    return time_series_fig, pie_fig, histogram_fig, data_table_fig, current_indicators


if __name__ == '__main__':
    app.run_server(debug=True)