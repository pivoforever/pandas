import pandas as pd
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

def parse_public_sheet(url, search_surname):
    # Преобразуем URL в формат для экспорта
    if '/edit#' in url:
        url = url.replace('/edit#', '/export?format=csv&')
    elif '/edit?' in url:
        url = url.replace('/edit?', '/export?format=csv&')
    else:
        # Если это обычная ссылка на просмотр
        parsed = urlparse(url)
        if 'spreadsheets' in parsed.path:
            # Извлекаем ID документа
            path_parts = parsed.path.split('/')
            doc_id = path_parts[3] if len(path_parts) > 3 else None
            if doc_id:
                url = f'https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv'
    
    try:
        # Загружаем данные
        df = pd.read_csv(url)
        df_filled = df.fillna('')
        
        # Ищем фамилию
        results = []
        i=0
        for col in df_filled.columns:
            matches = df_filled[df_filled[col].astype(str).str.contains(search_surname, case=False, na=False)]
            if not matches.empty:
                for idx, row in matches.iterrows():
                    dayOfWeek=idx
                    groupName=i
                    while df_filled['Unnamed: 0'][dayOfWeek]=='':
                        dayOfWeek-=1
                    while df_filled[df_filled.columns[groupName]][7]=='':
                        groupName-=1
                    results.append({
                        'row': idx + 2,  # +2 потому что pandas индексирует с 0, а заголовок - первая строка
                        'column': col,
                        'неделя': df_filled[col][8],
                        'день недели': df_filled['Unnamed: 0'][dayOfWeek],
                        'пара': df_filled['Unnamed: 2'][idx],
                        'группа': df_filled[df_filled.columns[groupName]][7],
                        'value': row[col]
                    })
            i+=1
        return results
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def create_icalendar_file(filename, events_data):
    """
    Создает iCalendar файл с событиями
    """
    with open(filename, 'w', encoding='utf-8') as file:
        # Заголовок календаря
        file.write("BEGIN:VCALENDAR\n")
        file.write("VERSION:2.0\n")
        
        # Записываем каждое событие
        for i, event in enumerate(events_data, 1):
            if event['неделя']==weekNumber:
                startDate=iso_week_to_date(2025,int(event['неделя'])+34, isoWeek[event['день недели'].strip()])
                startTime=startPair[event['пара']]
                start=startDate+'T'+startTime
                finishTime=finishPair[event['пара']]
                finish=startDate+'T'+finishTime
                file.write("BEGIN:VEVENT\n")
                file.write(f"DTSTART;TZID=Asia/Yekaterinburg:{start}\n")
                file.write(f"DTEND;TZID=Asia/Yekaterinburg:{finish}\n")
                file.write(f"SUMMARY:{event['группа']} {event['value']}\n")
                if 'location' in event:
                    file.write(f"LOCATION:{event['location']}\n")
                file.write("END:VEVENT\n")
        
        file.write("END:VCALENDAR\n")
    
    print(f"Файл {filename} создан успешно!")

def iso_week_to_date(year, week_number, day_of_week=1):
    """
    Использует ISO формат (понедельник=1, воскресенье=7)
    
    :param year: год
    :param week_number: номер недели ISO (1-53)
    :param day_of_week: день недели ISO (1=понедельник, 7=воскресенье)
    :return: дата в формате ГГГГ-ММ-ДД
    """
    # Первый день года
    first_day = datetime(year, 1, 1)
    
    # Если 1 января - пятница, суббота или воскресенье, то это 53 или 52 неделя предыдущего года
    if first_day.isoweekday() in [5, 6, 7] and week_number == 1:
        first_day = datetime(year-1, 12, 31)
        while first_day.isoweekday() != 1:  # Находим понедельник
            first_day += timedelta(days=1)
    else:
        # Находим первый понедельник года
        while first_day.isoweekday() != 1:
            first_day += timedelta(days=1)
    
    # Вычисляем дату
    target_date = first_day + timedelta(weeks=week_number-1, days=day_of_week-1)
    
    return target_date.strftime("%Y%m%d")


# Печать данных по курсу
def printData(results):
    for result in results:
        if result['неделя']==weekNumber:
            print(f"Строка: {result['row']}, Колонка: {result['column']}, Неделя: {result['неделя']}, День недели: {result['день недели']}, Группа: {result['группа']}, Пара: {result['пара']}, Значение: {result['value']}")

# Использование
isoWeek={'Понедельник':1,'Вторник':2,'Среда':3,'Четверг':4,'Пятница':5,'Суббота':6,'Воскресенье':7}
startPair={'1':'080000','2':'094000','3':'120000','4':'134000','5':'155000','6':'173000'}
finishPair={'1':'093000','2':'111000','3':'133000','4':'151000','5':'172000','6':'190000'}
teacherName=input('Введите фамилию преподавателя: ')
weekNumber=input('Введите номер недели: ')
results = parse_public_sheet("https://docs.google.com/spreadsheets/d/1Ojaq4ZG4qxRRxqPV9qXglT9zM0JIM079/edit?gid=744990727#gid=744990727", teacherName)+ parse_public_sheet("https://docs.google.com/spreadsheets/d/16ojS9myOnEOs8OFvJgjGglho-7aRMcV5/edit?gid=37242147#gid=37242147", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/16ojS9myOnEOs8OFvJgjGglho-7aRMcV5/edit?gid=447907294#gid=447907294", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/1rbUMw-YmpSBfNQPW5L6-C80BB9vvxx7l/edit?gid=394051115#gid=394051115", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/1rbUMw-YmpSBfNQPW5L6-C80BB9vvxx7l/edit?gid=493476051#gid=493476051", teacherName)
if teacherName.isnumeric():
    results+=parse_public_sheet("https://docs.google.com/spreadsheets/d/1Ojaq4ZG4qxRRxqPV9qXglT9zM0JIM079/edit?gid=98116459#gid=98116459", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/1Ojaq4ZG4qxRRxqPV9qXglT9zM0JIM079/edit?gid=31778361#gid=31778361", teacherName) +    parse_public_sheet("hhttps://docs.google.com/spreadsheets/d/1Ojaq4ZG4qxRRxqPV9qXglT9zM0JIM079/edit?gid=1353187888#gid=1353187888", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/1Ojaq4ZG4qxRRxqPV9qXglT9zM0JIM079/edit?gid=315466639#gid=315466639", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/16ojS9myOnEOs8OFvJgjGglho-7aRMcV5/edit?gid=1439101807#gid=1439101807", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/16ojS9myOnEOs8OFvJgjGglho-7aRMcV5/edit?gid=1100807409#gid=1100807409", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/16ojS9myOnEOs8OFvJgjGglho-7aRMcV5/edit?gid=22549204#gid=22549204", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/1rbUMw-YmpSBfNQPW5L6-C80BB9vvxx7l/edit?gid=1247167705#gid=1247167705", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/1rbUMw-YmpSBfNQPW5L6-C80BB9vvxx7l/edit?gid=354914518#gid=354914518", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/1rbUMw-YmpSBfNQPW5L6-C80BB9vvxx7l/edit?gid=980317130#gid=980317130", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/1rbUMw-YmpSBfNQPW5L6-C80BB9vvxx7l/edit?gid=1901193065#gid=1901193065", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/16ojS9myOnEOs8OFvJgjGglho-7aRMcV5/edit?gid=182080691#gid=182080691", teacherName) +    parse_public_sheet("https://docs.google.com/spreadsheets/d/16ojS9myOnEOs8OFvJgjGglho-7aRMcV5/edit?gid=2033152424#gid=2033152424", teacherName)


create_icalendar_file('myCalendar.ics', results)