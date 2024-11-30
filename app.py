import dash
from dash import dcc, html, Input, Output
from dash.dash_table import DataTable
import pandas as pd
import plotly.express as px
import base64
import io

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Основная структура дашборда с CSS стилями
app.layout = html.Div(style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.H1(children='Дашборд посещаемости веб-сайта', style={'textAlign': 'center', 'color': '#4A4A4A'}),

    # Форма для загрузки файла
    dcc.Upload(
        id='upload-data',
        children=html.Button('Загрузить CSV файл', style={'padding': '10px 20px', 'fontSize': '16px'}),
        multiple=False
    ),
    html.Div(id='output-data-upload', style={'marginTop': '10px', 'color': '#FF5733'}),

    # Компонент для выбора диапазона дат
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=pd.to_datetime('2024-01-01'),
        end_date=pd.to_datetime('2024-12-31'),
        display_format='YYYY-MM-DD',
        style={'marginTop': '20px'}
    ),

    # График временного ряда
    dcc.Graph(id='time-series-graph', style={'marginTop': '20px'}),

    # Круговая диаграмма
    dcc.Graph(id='pie-chart', style={'marginTop': '20px'}),

    # Гистограмма
    dcc.Graph(id='histogram', style={'marginTop': '20px'}),

    # Таблица с данными (сортируемая)
    DataTable(
        id='data-table',
        columns=[
            {'name': 'Дата', 'id': 'date', 'type': 'datetime'},
            {'name': 'Посещения', 'id': 'visits'},
            {'name': 'Уникальные посетители', 'id': 'unique_visitors'},
            {'name': 'Просмотры страниц', 'id': 'page_views'},
            {'name': 'Процент отказов', 'id': 'bounce_rate'},
            {'name': 'Категория', 'id': 'category'},
            {'name': 'Год', 'id': 'year'},
            {'name': 'Месяц', 'id': 'month'},
            {'name': 'Квартал', 'id': 'quarter'}
        ],
        sort_action='native',
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'border': '1px solid #ddd'
        },
        style_header={
            'backgroundColor': '#f5f5f5',
            'fontWeight': 'bold'
        },
        page_size=10  # Количество строк на странице
    ),

    # Индикаторы для отображения текущих значений показателей
    html.Div(id='current-indicators', style={'marginTop': '20px'})
])


# Функция для обработки загруженного файла
def parse_contents(contents):
    content_type, content_string = contents.split(',')

    # Декодирование содержимого файла
    decoded = base64.b64decode(content_string)

    # Чтение CSV файла в DataFrame
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Добавление столбцов для года, месяца и квартала
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter

    return df


# Обновление графиков и таблицы на основе загруженного файла и выбранного диапазона дат
@app.callback(
    [Output('output-data-upload', 'children'),
     Output('time-series-graph', 'figure'),
     Output('pie-chart', 'figure'),
     Output('histogram', 'figure'),
     Output('data-table', 'data'),
     Output('current-indicators', 'children')],
    [Input('upload-data', 'contents'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_output(contents, start_date, end_date):
    if contents is None:
        return "Пожалуйста, загрузите файл.", {}, {}, {}, [], []

    # Парсинг содержимого загруженного файла
    df = parse_contents(contents)

    # Фильтрация данных по выбранному диапазону дат
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    time_series_fig = px.line(filtered_df, x='date', y='visits', title='Посещения по времени')
    pie_fig = px.pie(filtered_df, names='category', values='visits', title='Структура посещений по категориям')
    histogram_fig = px.histogram(filtered_df, x='visits', nbins=20, title='Гистограмма посещений')

    # Передаем данные в таблицу в формате словаря
    data_table_data = filtered_df.to_dict('records')

    current_visits = filtered_df['visits'].sum()
    unique_visitors = filtered_df['unique_visitors'].sum()

    current_indicators = [
        html.Div(f'Текущие посещения: {current_visits}', style={'fontSize': 20}),
        html.Div(f'Количество уникальных посетителей: {unique_visitors}', style={'fontSize': 20}),
        html.Div(f'Общее количество просмотров страниц: {filtered_df["page_views"].sum()}', style={'fontSize': 20}),
        html.Div(f'Средний процент отказов: {filtered_df["bounce_rate"].mean():.2f}%', style={'fontSize': 20}),
    ]

    return "Файл успешно загружен.", time_series_fig, pie_fig, histogram_fig, data_table_data, current_indicators


if __name__ == '__main__':
    app.run_server(debug=True)