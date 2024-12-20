from datetime import datetime


def validate_date(date_str):
    # Проверка формата даты
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        return False
    
    # Проверка того, что дата находится в будущем
    if date <= datetime.now():
        return False
    
    # Проверка того, что дата не попадает на выходные дни
    if date.weekday() in {5, 6}:  # 5 - суббота, 6 - воскресенье
        return False
    
    return True