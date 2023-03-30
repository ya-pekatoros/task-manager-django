from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User, Task, Tag
from http import HTTPStatus
import datetime


class TestTaskViewSetNonAutorized(TestViewSetBase):
    basename = "tasks"

    def login(*args):
        return None

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.content

    def test_retrieve(self):
        response = self.retrieve(key=1)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.content

    def test_delete(self):
        response = self.delete(key=1)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.content

    def test_update(self):
        response = self.update(key=1, data={})
        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.content

    def test_create(self):
        response = self.create(data={})
        assert response.status_code == HTTPStatus.UNAUTHORIZED, response.content


class TestTaskViewSetAdmin(TestViewSetBase):
    basename = "tasks"
    user_attributes = {
        "username": "Test-admin",
        "name": "Test-admin",
        "surname": "Test-admin",
        "email": "test-admin@test.com",
        "password": "12345",
        "role": User.Roles.ADMIN,
        "avatar_picture": None,
    }
    user_2_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
        "avatar_picture": None,
    }
    user_3_attributes = {
        "username": "Test-manager",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
        "avatar_picture": None,
    }

    today = datetime.date.today().strftime("%Y-%m-%d")

    @classmethod
    def setUpTestData(cls):
        cls.user_2 = cls.create_api_user(cls.user_2_attributes)
        cls.user_3 = cls.create_api_user(cls.user_3_attributes)
        super().setUpTestData()

    def test_list(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_3,
            "executor": self.user_2,
        }
        task = self.create_task(task_attributes)

        task_2_attributes = {
            "title": "Test-task-2",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_3,
            "executor": self.user_2,
        }
        task_2 = self.create_task(task_2_attributes)

        response = self.list()
        expected_response = [self.get_expected_task_attr(task), self.get_expected_task_attr(task_2)]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_3,
            "executor": self.user_2,
        }
        task = self.create_task(task_attributes)

        response = self.retrieve(key=task.id)

        expected_response = self.get_expected_task_attr(task)

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_delete(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_3,
            "executor": self.user_2,
        }
        task = self.create_task(task_attributes)
        task_2_attributes = {
            "title": "Test-task-2",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_3,
            "executor": self.user_2,
        }
        task_2 = self.create_task(task_2_attributes)


        response = self.delete(key=task.id)
        response_list = self.list()
        expected_response_list = [
            self.get_expected_task_attr(task_2),
        ]

        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        assert response_list.json() == expected_response_list

    def test_update(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_3,
            "executor": self.user_2,
        }
        task = self.create_task(task_attributes)
        tag = Tag.objects.create(**{"title": "bug"})
        tag_2 = Tag.objects.create(**{"title": "feature"})

        task_attributes["title"] = "Test-task-updated"
        task_attributes["author"] = self.user_2.id
        task_attributes["executor"] = self.user_3.id
        task_attributes["tags"] = [tag, tag_2]

        response = self.update(key=task.id, data=task_attributes)
        response_dict = response.json()

        assert response.status_code == HTTPStatus.OK, response.content
        assert (
            Task.objects.get(id=task.id).author == self.user_3
        )  # author is still manager (the author is always the one who created the task)
        assert response_dict["title"] == task_attributes["title"]
        assert response_dict["executor"] == self.user_3.id
        assert response_dict["tags"] == [tag.title, tag_2.title]

    def test_create(self):
        tag = Tag.objects.create(**{"title": "bug"})
        data = {
            "title": "Test-task-2",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_2.id,
            "executor": self.user_3.id,
            "tags": [
                tag,
            ],
        }

        response = self.create(data)

        response_dict = response.json()

        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response_dict["tags"] == [
            tag.title,
        ]
        assert (
            response_dict["author"] == self.user.id
        )  # the author is always the one who created the task


class TestTaskViewSetManager(TestViewSetBase):
    basename = "tasks"
    user_attributes = {
        "username": "Test-manager",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
        "avatar_picture": None,
    }
    user_2_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
        "avatar_picture": None,
    }
    user_3_attributes = {
        "username": "Test-manager-1",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
        "avatar_picture": None,
    }

    @classmethod
    def setUpTestData(cls):
        cls.user_2 = cls.create_api_user(cls.user_2_attributes)
        cls.user_3 = cls.create_api_user(cls.user_3_attributes)
        super().setUpTestData()

    today = datetime.date.today().strftime("%Y-%m-%d")

    def test_list(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_3,
            "executor": self.user_2,
        }
        task = self.create_task(task_attributes)

        task_2_attributes = {
            "title": "Test-task-2",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_3,
            "executor": self.user_2,
        }
        task_2 = self.create_task(task_2_attributes)

        response = self.list()
        expected_response = [self.get_expected_task_attr(task), self.get_expected_task_attr(task_2)]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user,
            "executor": self.user_2,
        }

        task = self.create_task(task_attributes)

        response = self.retrieve(key=task.id)

        expected_response = self.get_expected_task_attr(task)

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_delete(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user,
            "executor": self.user_2,
        }

        task = self.create_task(task_attributes)

        response = self.delete(key=task.id)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user,
            "executor": self.user_2,
        }

        task = self.create_task(task_attributes)

        tag = Tag.objects.create(**{"title": "bug"})
        tag_2 = Tag.objects.create(**{"title": "feature"})

        task_attributes["tags"] = [tag, tag_2]
        task_attributes["executor"] = self.user_3.id
        task_attributes["description"] = "Test"
        task_attributes["title"] = "Test-task-updated"

        response = self.update(key=task.id, data=task_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

        del task_attributes["title"]
        del task_attributes["author"]

        response = self.update(key=task.id, data=task_attributes)
        response_dict = response.json()

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_dict["executor"] == self.user_3.id
        assert response_dict["tags"] == [tag.title, tag_2.title]

    def test_create(self):
        tag = Tag.objects.create(**{"title": "bug"})
        data = {
            "title": "Test-task-2",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "executor": self.user_3.id,
            "tags": [
                tag,
            ],
        }

        response = self.create(data)

        response_dict = response.json()

        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response_dict["title"] == data["title"]
        assert response_dict["tags"] == [
            tag.title,
        ]
        assert response_dict["author"] == self.user.id


class TestTaskViewSetDeveloper(TestViewSetBase):
    basename = "tasks"
    user_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
        "avatar_picture": None,
    }
    user_2_attributes = {
        "username": "Test-manager",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
        "avatar_picture": None,
    }

    today = datetime.date.today().strftime("%Y-%m-%d")

    @classmethod
    def setUpTestData(cls):
        cls.user_2 = cls.create_api_user(cls.user_2_attributes)
        super().setUpTestData()

    def test_list(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_2,
            "executor": self.user_2,
        }
        task = self.create_task(task_attributes)
 
        task_2_attributes = {
            "title": "Test-task-2",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_2,
            "executor": self.user_2,
        }
        task_2 = self.create_task(task_2_attributes)
 
        response = self.list()
        expected_response = [self.get_expected_task_attr(task), self.get_expected_task_attr(task_2)]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_2,
            "executor": self.user,
        }

        task = self.create_task(task_attributes)

        response = self.retrieve(key=task.id)
        expected_response = self.get_expected_task_attr(task)

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_delete(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_2,
            "executor": self.user,
        }

        task = self.create_task(task_attributes)

        response = self.delete(key=task.id)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update(self):
        task_attributes = {
            "title": "Test-task-1",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_2,
            "executor": self.user,
        }

        task = self.create_task(task_attributes)

        task_attributes["title"] = "Test-task-updated"
        tag = Tag.objects.create(**{"title": "bug"})
        tag_2 = Tag.objects.create(**{"title": "feature"})
        task_attributes["tags"] = [tag, tag_2]

        response = self.update(key=task.id, data=task_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

        response = self.update(
            key=task.id,
            data={
                "state": Task.States.IN_DEVELOPMENT,
                "tags": [tag.title, tag_2.title],
            },
        )

        response_dict = response.json()

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_dict["state"] == Task.States.IN_DEVELOPMENT
        assert response_dict["tags"] == [tag.title, tag_2.title]

    def test_create(self):
        response = self.create(data={})
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
