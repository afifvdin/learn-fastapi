from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6377/0")
celery_app.autodiscover_tasks(["app.tasks.email_tasks"])
