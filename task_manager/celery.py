from celery import Celery, states
from celery.signals import before_task_publish
from typing import Any


app = Celery("task_manager")
app.config_from_object("django.conf:settings", namespace="CELERY")


@before_task_publish.connect
def update_sent_state(sender: str = None, headers: dict = None, **kwargs: Any) -> None:
    task = app.tasks.get(sender)
    backend = task.backend if task else app.backend

    backend.store_result(headers["id"], None, states.STARTED)


if __name__ == "__main__":
    app.start()
