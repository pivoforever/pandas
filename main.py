import pandas as pd
import requests
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from diff import colored_diff

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
        gid = url.split('gid=')[-1] if 'gid=' in url else '0'
        
        # Ищем фамилию
        results = []
        groupName=sheet_names.get(gid, 'Неизвестный лист')
        for col in df_filled.columns:
            matches = df_filled[df_filled[col].astype(str).str.contains(search_surname, case=False, na=False)]
            if not matches.empty:
                for idx, row in matches.iterrows():
                    dayOfWeek=idx
                    while df_filled['День недели'][dayOfWeek]=='':
                        dayOfWeek-=1
                    results.append({
                        'row': idx + 2,  # +2 потому что pandas индексирует с 0, а заголовок - первая строка
                        'column': col,
                        'неделя': df_filled[col][0],
                        'день недели': df_filled['День недели'][dayOfWeek],
                        'пара': str(int(df_filled['№ пары'][idx])),
                        'группа': groupName,
                        'value': row[col]
                    })
        return results
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def create_icalendar_file(filename, events_data):
    """
    Создает iCalendar файл с событиями, переписывая предыдущие данные в файл iCalendar_old
    """
    os.remove('myCalendar_old.ics')
    os.rename(filename, 'myCalendar_old.ics')
    with open(filename, 'w', encoding='utf-8') as file:
        # Заголовок календаря
        file.write("BEGIN:VCALENDAR\n")
        file.write("VERSION:2.0\n")
        
        # Записываем каждое событие
        for i, event in enumerate(events_data, 1):
            week=int(event['неделя'])
            if week>=weekNumber and week<=weekNumberEnd:
                startDate=iso_week_to_date(2026,int(event['неделя'])-18, isoWeek[event['день недели'].strip()])
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
weekNumber=int(input('Введите с какой недели: '))
weekNumberEnd=int(input('Введите по какую неделю: '))
sheet_names = {
    '511325013': 'ИСП-2124',
    '744990727': 'ИСП-2224',
    '447907294': 'ИСП-(с)3223',
    '1405565128': 'ИСП-(с)3323',
    '1921378572': 'ИСП-(с)3423',
    '1346498076': 'ИСП-(с)3623',
    '1361637083': 'ИСП-(с)3723'
}

results = parse_public_sheet("https://docs.google.com/spreadsheets/d/1eLs6xDw60hpKogZY8mhR5wvnpV1hB5J_/edit?gid=511325013#gid=511325013", teacherName)+ parse_public_sheet("https://docs.google.com/spreadsheets/d/1eLs6xDw60hpKogZY8mhR5wvnpV1hB5J_/edit?gid=744990727#gid=744990727", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/1UFT2opdL3Xv5eIc6_vDF2eUoC4gtnl5-/edit?gid=447907294#gid=447907294", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/1UFT2opdL3Xv5eIc6_vDF2eUoC4gtnl5-/edit?gid=1405565128#gid=1405565128", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/1UFT2opdL3Xv5eIc6_vDF2eUoC4gtnl5-/edit?gid=1921378572#gid=1921378572", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/1UFT2opdL3Xv5eIc6_vDF2eUoC4gtnl5-/edit?gid=1346498076#gid=1346498076", teacherName) + parse_public_sheet("https://docs.google.com/spreadsheets/d/1UFT2opdL3Xv5eIc6_vDF2eUoC4gtnl5-/edit?gid=1361637083#gid=1361637083", teacherName)

""" events = [
    {
        'start': '20250924T230000',
        'end': '20250924T235000', 
        'title': 'Экспл. лаба ПИ-37 1п',
        'location': 'Авангард, 311'
    }
]
"""
create_icalendar_file('myCalendar.ics', results)
colored_diff('myCalendar_old.ics', 'myCalendar.ics')