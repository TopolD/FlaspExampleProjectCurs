from datetime import date, datetime
from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr
):
    email = EmailMessage()
    email["Subject"] = "Booking Confirmation"
    email["From"] = f"{settings.SMTP_USER}"
    email["To"] = email_to
    email.set_content(f"""
        <h1>Подтвердите бронирование,</h1>
        Вы забронировали отель c {booking['date_from']} по {booking['date_to']}
    """, subtype="html")

    return email


def create_remainder_confirmation_template(
        bookings: dict,
        email_to: EmailStr
):
    msgs = []
    current_date = datetime.date(datetime.now())
    for booking in bookings:


        dt = datetime.strptime(booking['date_from'], "%Y-%m-%d")
        days_left = (dt.date() - current_date).days

        if days_left in (1, 3):
            day_word = "день" if days_left == 1 else "дня"
            content = f"""
                       <h1>Напоминание о бронировании</h1>
                       <p>Напоминаем, что через {days_left} {day_word} у вас забронирован отель на такую дату: {booking['date_to']}</p>
                   """

            email = EmailMessage()
            email["Subject"] = "Remainder Confirmation"
            email["From"] = f"{settings.SMTP_USER}"
            email["To"] = email_to
            email.set_content(content, subtype="html")
            msgs.append(email)
    return msgs
