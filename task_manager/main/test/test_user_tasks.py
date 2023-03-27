from http import HTTPStatus
import datetime
from django.urls import reverse

from typing import Union

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User, Task
from task_manager.main.test.factories.user import UserFactory


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"
    user_attributes = UserFactory.build(role=User.Roles.ADMIN)
    today = datetime.date.today().strftime("%Y-%m-%d")

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[*key])


    def test_list(self) -> None:
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user,
            "executor": self.user,
        }
        task = self.create_task(task_attributes)

        response = self.list(args=[self.user.id])
        expected_response = [self.get_expected_task_attr(task),]

        assert response.json() == expected_response

    def test_retrieve_foreign_task(self) -> None:
        another_user_attributes = UserFactory.build(role=User.Roles.ADMIN)
        another_user = self.create_api_user(another_user_attributes)
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user,
            "executor": another_user,
        }
        task = self.create_task(task_attributes)

        response = self.retrieve(key=[self.user.id, task.id])

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user,
            "executor": self.user,
        }
        task = self.create_task(task_attributes)

        expected_response = self.get_expected_task_attr(task)

        response = self.retrieve(key=[self.user.id, task.id])

        assert response.json() == expected_response
