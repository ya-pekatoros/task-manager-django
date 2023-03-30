import datetime

from task_manager.main.models import User, Task
from task_manager.main.test.base import TestViewSetBase
from task_manager.main.test.factories.user import UserFactory


class TestUserTasksViewSet(TestViewSetBase):
    basename = "task_tags"
    user_attributes = UserFactory.build(role=User.Roles.ADMIN)
    today = datetime.date.today().strftime("%Y-%m-%d")

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

        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)
        tag_2_attributes = {"title": "feature"}
        tag_2 = self.create_tag(tag_2_attributes)

        task.tags.add(tag)
        task.tags.add(tag_2)
        task.save()

        response = self.list(args=[task.id])

        expected_response = [self.get_expected_tag_attr(tag), self.get_expected_tag_attr(tag_2)]

        assert response.json() == expected_response
