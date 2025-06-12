from app.exceptions import LargeDateFromHttpException, UnableToBookDate
from datetime import date

def calculate_day(date_from, date_to):

    if date_from >= date_to:
        raise LargeDateFromHttpException

    result = abs((date_to - date_from).days)

    if result > 30:
        raise UnableToBookDate




