from django.utils import timezone
import calendar
from datetime import datetime

def datetime_context(request):
    """Передаёт в шаблоны текущую дату, время, календарь и таймзону"""
    
    # Получаем часовой пояс пользователя из сессии или используем стандартный
    user_tz_str = request.session.get('timezone', 'Europe/Minsk')
    
    # Активируем часовой пояс для текущего запроса
    timezone.activate(user_tz_str)
    
    # Текущее время в активированной таймзоне
    user_now = timezone.localtime(timezone.now())
    
    # UTC время
    utc_now = timezone.now()
    
    # Форматирование дат
    user_date_str = user_now.strftime('%d/%m/%Y')
    user_datetime_str = user_now.strftime('%d/%m/%Y %H:%M:%S')
    utc_datetime_str = utc_now.strftime('%d/%m/%Y %H:%M:%S')
    
    # Текстовый календарь на текущий месяц
    cal = calendar.monthcalendar(user_now.year, user_now.month)
    
    month_names = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    
    return {
        'user_timezone': user_tz_str,
        'user_now': user_now,
        'user_date': user_date_str,
        'user_datetime': user_datetime_str,
        'utc_datetime': utc_datetime_str,
        'calendar_month': month_names[user_now.month],
        'calendar_year': user_now.year,
        'calendar_weeks': cal,
    }