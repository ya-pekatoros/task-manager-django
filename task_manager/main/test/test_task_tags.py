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

        del self.user_attributes["password"]
        task_attributes["author"] = self.user_attributes
        task_attributes["id"] = task.id
        task_attributes["executor"] = self.user_attributes
        task_attributes["executor"]["id"] = self.user.id
        task_attributes["author"]["id"] = self.user.id
        task_attributes["author"]["role"] = "admin"
        task_attributes["author"]["avatar_picture"] = (
            "http://testserver" + self.user.avatar_picture.url
        )
        task_attributes["executor"]["role"] = "admin"
        task_attributes["executor"]["avatar_picture"] = (
            "http://testserver" + self.user.avatar_picture.url
        )
        task_attributes["priority"] = "middle"
        task_attributes["state"] = "new task"
        task_attributes["created_at"] = self.today
        task_attributes["edited_at"] = self.today
        task_attributes["tags"] = [tag.title, tag_2.title]

        tag_attributes["tasks"] = [task_attributes]
        tag_attributes["id"] = tag.id
        tag_2_attributes["tasks"] = [task_attributes]
        tag_2_attributes["id"] = tag_2.id

        task.tags.add(tag)
        task.tags.add(tag_2)
        task.save()

        response = self.list(args=[task.id])

        assert response.json() == [tag_attributes, tag_2_attributes]
