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
        with open('file.txt', 'a', encoding='utf-8') as file:
            print(df_filled.head(10), file=file)
            print(df_filled.columns, file=file)

        gid = url.split('gid=')[-1] if 'gid=' in url else '0'
        sheet_names = {
            '511325013': 'ИСП-2124',
            '744990727': 'ИСП-2224',
            '447907294': 'ИСП-(с)3223',
            '1405565128': 'ИСП-(с)3323',
            '1921378572': 'ИСП-(с)3423',
            '1346498076': 'ИСП-(с)3623',
            '1361637083': 'ИСП-(с)3723'
        }
        
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
                        'пара': df_filled['№ пары'][idx],
                        'группа': groupName,
                        'value': row[col]
                    })
        return results
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

isoWeek={'Понедельник':1,'Вторник':2,'Среда':3,'Четверг':4,'Пятница':5,'Суббота':6,'Воскресенье':7}
startPair={'1':'080000','2':'094000','3':'120000','4':'134000','5':'155000','6':'173000'}
finishPair={'1':'093000','2':'111000','3':'133000','4':'151000','5':'172000','6':'190000'}
teacherName=input('Введите фамилию преподавателя: ')
weekNumber=int(input('Введите с какой недели: '))
weekNumberEnd=int(input('Введите по какую неделю: '))
results = parse_public_sheet("https://docs.google.com/spreadsheets/d/1eLs6xDw60hpKogZY8mhR5wvnpV1hB5J_/edit?gid=511325013#gid=511325013", teacherName)