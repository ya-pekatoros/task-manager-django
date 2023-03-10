from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User
from http import HTTPStatus


class TestTagViewSetNonAutorized(TestViewSetBase):
    basename = "tags"

    def login(*args):
        return None

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_retrieve(self):
        response = self.retrieve(key=1)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_delete(self):
        response = self.delete(key=1)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update(self):
        response = self.update(key=1, data={})
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_create(self):
        response = self.create(data={})
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content


class TestTagViewSetAdmin(TestViewSetBase):
    basename = "tags"
    user_attributes = {
        "username": "Test-admin",
        "name": "Test-admin",
        "surname": "Test-admin",
        "email": "test-admin@test.com",
        "password": "12345",
        "role": User.Roles.ADMIN,
    }
    tag_attributes = {"title": "bug"}

    def test_create(self):
        data = self.tag_attributes
        response = self.create(data=data)
        data["tasks"] = []
        expected_response = self.expected_details(response, data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response.json() == expected_response

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        self.tag_attributes["tasks"] = []
        expected_response = self.expected_details(response, self.tag_attributes)
        assert response.json()[0] == expected_response
        self.tag_attributes["id"] = expected_response["id"]

    def test_retrieve(self):
        response = self.retrieve(key=self.tag_attributes["id"])
        assert response.json() == self.tag_attributes

    def test_update(self):
        self.tag_attributes["title"] = "bug-updated"
        id = self.tag_attributes["id"]
        del self.tag_attributes["id"]
        response = self.update(key=id, data=self.tag_attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        self.tag_attributes["id"] = id
        assert response.json() == self.tag_attributes

    def test_delete(self):
        object_data = self.list().json()[0]
        id = object_data["id"]
        response = self.delete(key=id)
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content


class TestTagViewSetAdmin(TestViewSetBase):
    basename = "tags"
    user_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
    }
    tag_attributes = {"title": "bug"}

    def test_create(self):
        data = self.tag_attributes
        response = self.create(data=data)
        data["tasks"] = []
        expected_response = self.expected_details(response, data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response.json() == expected_response

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        self.tag_attributes["tasks"] = []
        expected_response = self.expected_details(response, self.tag_attributes)
        assert response.json()[0] == expected_response
        self.tag_attributes["id"] = expected_response["id"]

    def test_retrieve(self):
        response = self.retrieve(key=self.tag_attributes["id"])
        assert response.json() == self.tag_attributes

    def test_update(self):
        self.tag_attributes["title"] = "bug-updated"
        id = self.tag_attributes["id"]
        del self.tag_attributes["id"]
        response = self.update(key=id, data=self.tag_attributes)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        self.tag_attributes["id"] = id

    def test_delete(self):
        object_data = self.list().json()[0]
        id = object_data["id"]
        response = self.delete(key=id)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content


class TestTagViewSetManager(TestViewSetBase):
    basename = "tags"
    user_attributes = {
        "username": "Test-manager",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
    }
    tag_attributes = {"title": "bug"}

    def test_create(self):
        data = self.tag_attributes
        response = self.create(data=data)
        data["tasks"] = []
        expected_response = self.expected_details(response, data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response.json() == expected_response

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        self.tag_attributes["tasks"] = []
        expected_response = self.expected_details(response, self.tag_attributes)
        assert response.json()[0] == expected_response
        self.tag_attributes["id"] = expected_response["id"]

    def test_retrieve(self):
        response = self.retrieve(key=self.tag_attributes["id"])
        assert response.json() == self.tag_attributes

    def test_update(self):
        self.tag_attributes["title"] = "bug-updated"
        id = self.tag_attributes["id"]
        del self.tag_attributes["id"]
        response = self.update(key=id, data=self.tag_attributes)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        self.tag_attributes["id"] = id

    def test_delete(self):
        object_data = self.list().json()[0]
        id = object_data["id"]
        response = self.delete(key=id)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
