function deleteCalendarEvents() {
    var calendarId = 'your-calendar-id@gmail.com'; // ID календаря
    var calendar = CalendarApp.getCalendarById(calendarId);

    // Удалить события за определенный период
    var startDate = new Date('2024-01-01');
    var endDate = new Date('2024-12-31');
    var events = calendar.getEvents(startDate, endDate);

    // Удалить все события в периоде
    for (var i = 0; i < events.length; i++) {
        events[i].deleteEvent();
        Logger.log('Удалено событие: ' + events[i].getTitle());
    }
}

// Удалить события по названию
function deleteEventsByTitle() {
    var calendar = CalendarApp.getDefaultCalendar();
    var events = calendar.getEvents(new Date('2024-01-01'), new Date('2024-12-31'));

    for (var i = 0; i < events.length; i++) {
        if (events[i].getTitle() === 'Экспл. лаба ПИ-37 1п') {
            events[i].deleteEvent();
            Logger.log('Удалено: ' + events[i].getTitle());
        }
    }
}