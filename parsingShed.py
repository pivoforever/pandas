import pandas as pd
import requests
from urllib.parse import urlparse, parse_qs

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

# Использование
results = parse_public_sheet("https://docs.google.com/spreadsheets/d/1Ojaq4ZG4qxRRxqPV9qXglT9zM0JIM079/edit?gid=744990727#gid=744990727", "Будилов")
weekNumber=input('Введите номер недели: ')
for result in results:
    if result['неделя']==weekNumber:
        print(f"Строка: {result['row']}, Колонка: {result['column']}, Неделя: {result['неделя']}, День недели: {result['день недели']}, Группа: {result['группа']}, Пара: {result['пара']}, Значение: {result['value']}")