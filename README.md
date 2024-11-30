# Дашборд анализа данных о посещении сайта

Этот дашборд позволяет анализировать данные о посещаемости веб-сайта с помощью интерактивных графиков и таблиц. Вы можете загружать данные в формате CSV и визуализировать их по различным метрикам.

## Установка

1. Убедитесь, что у вас установлен Python и необходимые библиотеки. Вы можете установить их с помощью pip:


> ***pip install dash pandas***


2. Скачайте или клонируйте репозиторий:
> ***git clone*** <https://github.com/SmurW632/DashboardSiteVisitors.git>
> ***cd <папка_репозитория>***


3. Запустите приложение:
> ***python <запускаемый_файл>.py***


4. Откройте браузер и перейдите по адресу http://127.0.0.1:8050.

## Использование
### Загрузка данных
1. Нажмите кнопку «Загрузить CSV-файл» и выберите файл с данными о посещаемости.
2. Файл должен быть в формате CSV и содержать следующие столбцы:
- **date**: Дата посещения (формат: YYYY-MM-DD)
- **visits**: Общее количество посещений за день
- **unique_visitors**: Количество уникальных посетителей за день
- **page_views**: Общее количество просмотров страниц за день
- **bounce_rate**: Процент отказов (в процентах)
- **category**: Категория веб-сайта


### Выбор диапазона дат
- **Используйте** компонент «Выбор диапазона дат» для фильтрации данных по определенному диапазону дат.
- **Выберите** начальную и конечную даты для анализа.
- 
### Графики
После загрузки файла и выбора диапазона дат, вы увидите следующие графики:
1. График временного ряда:
- Отображает количество посещений по времени.
- Позволяет анализировать тренды посещаемости.
2. Круговая диаграмма:
- Визуализирует структуру посещений по категориям.
- Позволяет увидеть долю каждой категории в общем количестве посещений.
3. Гистограмма:
- Показывает распределение количества посещений.
- Позволяет анализировать, как часто происходят различные уровни посещаемости.

## Таблица данных 
Таблица отображает все загруженные данные с возможностью сортировки.
Столбцы таблицы включают:
- Дата
- Посещения
- Уникальные посетители
- Просмотры страниц
- Процент отказов
- Категория
- Год
- Месяц
- Квартал

## Индикаторы текущих значений
Под таблицей отображаются текущие значения:
- Общее количество посещений за выбранный период.
- Количество уникальных посетителей.
- Общее количество просмотров страниц.
- Средний процент отказов.

## Примечания
- Убедитесь, что ваши данные корректны и соответствуют указанным выше требованиям.
- Если у вас возникли вопросы или предложения, не стесняйтесь обращаться!
