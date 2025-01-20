from datetime import datetime
import logging 


logger = logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def validate_date(date_str) -> datetime | str:
    # Проверка формата даты
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y')
       
        # Проверка того, что дата находится в будущем
        if date <= datetime.now():
            logging.error("Wrong date - past")
            return "Past"
        
        # Проверка того, что дата не попадает на выходные дни
        if date.weekday() in {5, 6}:  # 5 - суббота, 6 - воскресенье
            logging.error("Wrong date - weekend")
            return "Weekend"
    
    except ValueError:
        logging.error("Wrong date - format")
        return "WrongFormat"
    
    return date