from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange


from app.config import settings


celery_app = Celery(
    'tasks',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled"
     ]
)
celery_app.conf.beat_schedule = {
    "Reservation reminder":{
        "task":"remainder_task",
        "schedule":120
        # "schedule": crontab(minute=0, hour=9,),
    }
}
celery_app.conf.timezone = "UTC"
# celery_app.conf.task_queues = (
#     Queue('high', Exchange('high'), routing_key='high'),
#     Queue('medium', Exchange('medium'), routing_key='medium'),
#     Queue('low', Exchange('low'), routing_key='low'),
# )
#
# celery_app.conf.task_routes = {
#     'app.tasks.task_important': {'queue': 'high'},
#     'app.tasks.task_regular': {'queue': 'medium'},
#     'app.tasks.task_background': {'queue': 'low'},
# }