from django.db import models
from django.core.exceptions import ValidationError

from task_manager.main.models.tag import Tag
from task_manager.main.models.user import User


class Task(models.Model):
    class State(models.TextChoices):
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
    edited_at = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    status = models.CharField(
        max_length=255, default=State.NEW, choices=State.choices
    )
    priority = models.CharField(max_length=255, choices=Priorities.choices)
    tags = models.ManyToManyField(Tag)

    def clean(self):
        if self.pk:
            old_task = Task.objects.get(pk=self.pk)
            if old_task.status == self.State.NEW:
                if self.status not in [
                    self.State.IN_DEVELOPMENT,
                    self.State.ARCHIVED,
                ]:
                    raise ValidationError("Invalid status transition")
            elif old_task.status == self.State.IN_DEVELOPMENT:
                if self.status != self.State.IN_QA:
                    raise ValidationError("Invalid status transition")
            elif old_task.status == self.State.IN_QA:
                if self.status not in [
                    self.State.IN_DEVELOPMENT,
                    self.State.IN_CODE_REVIEW,
                ]:
                    raise ValidationError("Invalid status transition")
            elif old_task.status == self.State.IN_CODE_REVIEW:
                if self.status not in [
                    self.State.READY_FOR_RELEASE,
                    self.State.IN_DEVELOPMENT,
                ]:
                    raise ValidationError("Invalid status transition")
            elif old_task.status == self.State.READY_FOR_RELEASE:
                if self.status != self.State.RELEASED:
                    raise ValidationError("Invalid status transition")
            elif old_task.status == self.State.RELEASED:
                if self.status != self.State.ARCHIVED:
                    raise ValidationError("Invalid status transition")
            elif old_task.status == self.State.ARCHIVED:
                if self.status != self.State.ARCHIVED:
                    raise ValidationError("Invalid status transition")
