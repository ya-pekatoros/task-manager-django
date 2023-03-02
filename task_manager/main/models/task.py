from django.db import models
from django.core.exceptions import ValidationError

from task_manager.main.models.tag import Tag
from task_manager.main.models.user import User


class Task(models.Model):
    class States(models.TextChoices):
        NEW = "new task"
        IN_DEVELOPMENT = "in development"
        IN_QA = "in qa"
        IN_CODE_REVIEW = "in code review"
        READY_FOR_RELEASE = "ready for release"
        RELEASED = "released"
        ARCHIVED = "archived"

    class Priorities(models.TextChoices):
        HIGH = "high"
        MIDDLE = "middle"
        LOW = "low"

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="task_author"
    )
    executor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="task_executor"
    )
    description = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    edited_at = models.DateField(auto_now=True)
    deadline = models.DateField(null=True)
    state = models.CharField(max_length=255, default=States.NEW, choices=States.choices)
    priority = models.CharField(max_length=255, null=True, choices=Priorities.choices)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def clean(self):
        if self.pk:
            old_task = Task.objects.get(pk=self.pk)
            if self.state != old_task.state:
                if old_task.state == self.States.NEW:
                    if self.state not in [
                        self.States.IN_DEVELOPMENT,
                        self.States.ARCHIVED,
                    ]:
                        raise ValidationError("Invalid status transition")
                elif old_task.state == self.States.IN_DEVELOPMENT:
                    if self.state != self.States.IN_QA:
                        raise ValidationError("Invalid status transition")
                elif old_task.state == self.States.IN_QA:
                    if self.state not in [
                        self.States.IN_DEVELOPMENT,
                        self.States.IN_CODE_REVIEW,
                    ]:
                        raise ValidationError("Invalid status transition")
                elif old_task.state == self.States.IN_CODE_REVIEW:
                    if self.state not in [
                        self.States.READY_FOR_RELEASE,
                        self.States.IN_DEVELOPMENT,
                    ]:
                        raise ValidationError("Invalid status transition")
                elif old_task.state == self.States.READY_FOR_RELEASE:
                    if self.state != self.States.RELEASED:
                        raise ValidationError("Invalid status transition")
                elif old_task.state == self.States.RELEASED:
                    if self.state != self.States.ARCHIVED:
                        raise ValidationError("Invalid status transition")
                elif old_task.state == self.States.ARCHIVED:
                    raise ValidationError("Invalid status transition")
