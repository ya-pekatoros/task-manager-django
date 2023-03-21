import os
from celery import Celery

app = Celery("task_manager")
app.config_from_object("django.conf:settings", namespace="CELERY")

if __name__ == "__main__":
    app.start()
