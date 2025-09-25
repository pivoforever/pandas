from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # Правильный импорт
from googleapiclient.discovery import build
import os

def delete_google_calendar_events(credentials_file='credentials.json'):
    """
    Удаление событий через Google Calendar API
    """
    # Авторизация
    creds = None
    # Файл token.json сохраняет доступ после первой авторизации
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    
    # Если нет валидных credentials, запрашиваем авторизацию
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Создаем flow для OAuth авторизации
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, 
                ['https://www.googleapis.com/auth/calendar']
            )
            creds = flow.run_local_server(port=0)
        
        # Сохраняем credentials для будущего использования
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Создаем сервис для работы с Calendar API
    service = build('calendar', 'v3', credentials=creds)
    
    # Получаем список событий
    events_result = service.events().list(
        calendarId='primary',  # основной календарь
        timeMin='2025-01-01T00:00:00Z',
        timeMax='2025-12-31T23:59:59Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        print('События не найдены.')
        return
    
    # Удаляем события по условию
    deleted_count = 0
    for event in events:
        event_title = event.get('summary', 'Без названия')
        
        # Пример условия - удаляем события с определенным текстом
        if 'Старцева' in event_title:
            try:
                service.events().delete(
                    calendarId='primary',
                    eventId=event['id']
                ).execute()
                print(f"✅ Удалено: {event_title}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Ошибка при удалении {event_title}: {e}")
    
    print(f"\nУдаление завершено. Удалено событий: {deleted_count}")

# Использование
if __name__ == "__main__":
    delete_google_calendar_events()