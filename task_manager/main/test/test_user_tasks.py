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

        task_expected_attr = {
            "id": task.id,
            "author": self.user_attributes.copy(),
            "executor": self.user_attributes.copy(),
            "created_at": self.today,
            "edited_at": self.today,
            "tags": [],
            "state": task_attributes["state"].value,
            "priority": task_attributes["priority"].value,
        }
        task_attributes.update(task_expected_attr)

        del task_attributes["author"]["password"]
        task_attributes["author"]["role"] = self.user_attributes["role"].value
        task_attributes["author"]["id"] = self.user.id
        task_attributes["author"]["avatar_picture"] = (
            "http://testserver" + self.user.avatar_picture.url
        )

        del task_attributes["executor"]["password"]
        task_attributes["executor"]["role"] = self.user_attributes["role"].value
        task_attributes["executor"]["id"] = self.user.id
        task_attributes["executor"]["avatar_picture"] = (
            "http://testserver" + self.user.avatar_picture.url
        )

        response = self.list(args=[self.user.id])
        expected_response = [task_attributes]

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

        task_expected_attr = {
            "id": task.id,
            "author": self.user_attributes.copy(),
            "executor": self.user_attributes.copy(),
            "created_at": self.today,
            "edited_at": self.today,
            "tags": [],
            "state": task_attributes["state"].value,
            "priority": task_attributes["priority"].value,
        }
        task_attributes.update(task_expected_attr)

        del task_attributes["author"]["password"]
        task_attributes["author"]["role"] = self.user_attributes["role"].value
        task_attributes["author"]["id"] = self.user.id
        task_attributes["author"]["avatar_picture"] = (
            "http://testserver" + self.user.avatar_picture.url
        )

        del task_attributes["executor"]["password"]
        task_attributes["executor"]["role"] = self.user_attributes["role"].value
        task_attributes["executor"]["id"] = self.user.id
        task_attributes["executor"]["avatar_picture"] = (
            "http://testserver" + self.user.avatar_picture.url
        )

        response = self.retrieve(key=[self.user.id, task.id])
        expected_response = task_attributes

        assert response.json() == expected_response
