from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User, Task, Tag
from http import HTTPStatus
import json


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
    }
    tag_attributes = {"title": "bug"}
    task_attributes = {
        "title": "Test-task-1",
        "description": "Test",
        "deadline": "2023-07-05",
        "state": Task.States.NEW,
        "priority": Task.Priorities.MIDDLE,
    }
    user_2_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
    }

    user_3_attributes = {
        "username": "Test-manager",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
    }

    @classmethod
    def setUpTestData(cls):
        cls.user_2 = cls.create_api_user(cls.user_2_attributes)
        cls.user_3 = cls.create_api_user(cls.user_3_attributes)
        cls.task_attributes["author"] = cls.user_3
        cls.task_attributes["executor"] = cls.user_2
        super().setUpTestData()

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        response_dict = json.loads(response.content.decode("utf-8"))[0]
        assert response_dict["title"] == self.task_attributes["title"]
        assert response_dict["author"]["email"] == self.user_3_attributes["email"]
        self.task_attributes["id"] = response_dict["id"]

    def test_retrieve(self):
        response = self.retrieve(key=self.task_attributes["id"])
        assert response.status_code == HTTPStatus.OK, response.content
        response_dict = json.loads(response.content.decode("utf-8"))
        assert response_dict["title"] == self.task_attributes["title"]
        assert response_dict["author"]["email"] == self.user_3_attributes["email"]

    def test_delete(self):
        object_data = json.loads(self.list().content.decode("utf-8"))[0]
        id = object_data["id"]
        response = self.delete(key=id)
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content

    def test_update(self):
        self.task_attributes["title"] = "Test-task-updated"
        self.task_attributes["author"] = self.user_2.id
        self.task_attributes["executor"] = self.user_3.id

        id = self.task_attributes["id"]
        del self.task_attributes["id"]

        tag_2 = Tag.objects.create(**{"title": "feature"})

        self.task_attributes["tags"] = [self.tag, tag_2]

        response = self.update(key=id, data=self.task_attributes)

        self.task_attributes["id"] = id
        response_dict = json.loads(response.content.decode("utf-8"))

        assert response.status_code == HTTPStatus.OK, response.content
        assert (
            Task.objects.get(id=id).author == self.user_3
        )  # author is still manager (the author is always
        assert (
            response_dict["title"] == self.task_attributes["title"]
        )  # the one who created the task)
        assert response_dict["executor"] == self.user_3.id
        assert response_dict["tags"] == [self.tag.title, tag_2.title]

    def test_create(self):
        data = {
            "title": "Test-task-2",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "author": self.user_2.id,
            "executor": self.user_3.id,
            "tags": [
                self.tag,
            ],
        }

        response = self.create(data)

        response_dict = json.loads(response.content.decode("utf-8"))

        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response_dict["tags"] == [
            self.tag.title,
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
    }
    tag_attributes = {"title": "bug"}
    task_attributes = {
        "title": "Test-task-1",
        "description": "Test",
        "deadline": "2023-07-05",
        "state": Task.States.NEW,
        "priority": Task.Priorities.MIDDLE,
    }
    user_2_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
    }

    user_3_attributes = {
        "username": "Test-manager-1",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
    }

    @classmethod
    def setUpTestData(cls):
        cls.user_2 = cls.create_api_user(cls.user_2_attributes)
        cls.user_3 = cls.create_api_user(cls.user_3_attributes)
        cls.task_attributes["executor"] = cls.user_2
        super().setUpTestData()
        cls.task_attributes["author"] = cls.user
        cls.task.author = cls.user
        cls.task.save()
        cls.task_attributes["id"] = cls.task.id

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        response_dict = json.loads(response.content.decode("utf-8"))[0]
        assert response_dict["title"] == self.task_attributes["title"]
        assert response_dict["author"]["email"] == self.user_attributes["email"]

    def test_retrieve(self):
        response = self.retrieve(key=self.task_attributes["id"])
        assert response.status_code == HTTPStatus.OK, response.content
        response_dict = json.loads(response.content.decode("utf-8"))
        assert response_dict["title"] == self.task_attributes["title"]
        assert response_dict["author"]["email"] == self.user_attributes["email"]

    def test_delete(self):
        object_data = json.loads(self.list().content.decode("utf-8"))[0]
        id = object_data["id"]
        response = self.delete(key=id)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! обновить!!!!!!!! проверить что можем менять исполнителя, не можем менять автора
    # не можем менять название?

    def test_update(self):
        tag_2 = Tag.objects.create(**{"title": "feature"})

        data = {
            "title": "Test-task-updated",
            "executor": self.user_3.id,
            "description": "Test",
            "deadline": self.task_attributes["deadline"],
            "priority": self.task_attributes["priority"],
            "tags": [self.tag, tag_2],
            "state": self.task_attributes["state"],
        }

        response = self.update(key=self.task.id, data=data)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

        del data["title"]

        response = self.update(key=self.task.id, data=data)
        response_dict = json.loads(response.content.decode("utf-8"))

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_dict["executor"] == self.user_3.id
        assert response_dict["tags"] == [self.tag.title, tag_2.title]

    def test_create(self):
        data = {
            "title": "Test-task-2",
            "description": "Test",
            "deadline": "2023-07-05",
            "state": Task.States.NEW,
            "priority": Task.Priorities.MIDDLE,
            "executor": self.user_3.id,
            "tags": [
                self.tag,
            ],
        }

        response = self.create(data)

        response_dict = json.loads(response.content.decode("utf-8"))

        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response_dict["title"] == data["title"]
        assert response_dict["tags"] == [
            self.tag.title,
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
    }
    tag_attributes = {"title": "bug"}
    task_attributes = {
        "title": "Test-task-1",
        "description": "Test",
        "deadline": "2023-07-05",
        "state": Task.States.NEW,
        "priority": Task.Priorities.MIDDLE,
    }
    user_2_attributes = {
        "username": "Test-manager",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
    }

    @classmethod
    def setUpTestData(cls):
        cls.user_2 = cls.create_api_user(cls.user_2_attributes)
        cls.task_attributes["author"] = cls.user_2
        super().setUpTestData()
        cls.task_attributes["executor"] = cls.user
        cls.task_attributes["id"] = cls.task.id
        cls.task.executor = cls.user
        cls.task.save()

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        response_dict = json.loads(response.content.decode("utf-8"))[0]
        assert response_dict["title"] == self.task_attributes["title"]
        assert response_dict["author"]["email"] == self.user_2_attributes["email"]

    def test_retrieve(self):
        response = self.retrieve(key=self.task_attributes["id"])
        assert response.status_code == HTTPStatus.OK, response.content
        response_dict = json.loads(response.content.decode("utf-8"))
        assert response_dict["title"] == self.task_attributes["title"]
        assert response_dict["author"]["email"] == self.user_2_attributes["email"]

    def test_delete(self):
        response = self.delete(key=self.task_attributes["id"])
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update(self):
        self.task_attributes["title"] = "Test-task-updated"

        id = self.task_attributes["id"]
        del self.task_attributes["id"]

        tag_2 = Tag.objects.create(**{"title": "feature"})
        self.task_attributes["tags"] = [self.tag, tag_2]

        response = self.update(key=id, data=self.task_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

        print(self.task.executor)
        response = self.update(
            key=id,
            data={
                "state": Task.States.IN_DEVELOPMENT,
                "tags": [self.tag.title, tag_2.title],
            },
        )

        self.task_attributes["id"] = id

        response_dict = json.loads(response.content.decode("utf-8"))

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_dict["state"] == Task.States.IN_DEVELOPMENT
        assert response_dict["tags"] == [self.tag.title, tag_2.title]

    def test_create(self):
        response = self.create(data={})
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
