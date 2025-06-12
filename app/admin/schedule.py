from app.tasks.celery_app import celery_app



@celery_app.task(
    name="send_remainder_for_bookings"
)
def send_remainder_for_bookings():
    pass