from datetime import datetime, timedelta

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

# Примеры
print(iso_week_to_date(2025, 38, 4))