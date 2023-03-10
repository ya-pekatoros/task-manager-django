from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User
from http import HTTPStatus


class TestUserViewSetAdmin(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "Test-admin",
        "name": "Test-admin",
        "surname": "Test-admin",
        "email": "test-admin@test.com",
        "password": "12345",
        "role": User.Roles.ADMIN,
    }

    def test_create(self):
        response = self.create(data={})
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        del self.user_attributes["password"]
        self.user_attributes["role"] = "admin"
        expected_response = self.expected_details(
            response, self.user_attributes
        )
        assert response.json()[0] == expected_response
        self.user_attributes["id"] = expected_response["id"]

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])
        self.user_attributes["role"] = "admin"
        assert response.json() == self.user_attributes

    def test_update(self):
        self.user_attributes["name"] = "Test-admin-updated"
        self.user_attributes["role"] = User.Roles.MANAGER
        id = self.user_attributes["id"]
        del self.user_attributes["id"]
        response = self.update(key=id, data=self.user_attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        self.user_attributes["role"] = "manager"
        self.user_attributes["id"] = id
        assert response.json() == self.user_attributes

    def test_delete(self):
        object_data = self.list().json()[0]
        id = object_data["id"]
        response = self.delete(key=id)
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content


class TestUserViewSetDeveloper(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
    }

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        del self.user_attributes["password"]
        self.user_attributes["role"] = "developer"
        expected_response = self.expected_details(
            response, self.user_attributes
        )
        assert response.json()[0] == expected_response
        self.user_attributes["id"] = expected_response["id"]

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])
        assert response.json() == self.user_attributes

    def test_create(self):
        response = self.create(data={})
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_role(self):
        self.user_attributes["name"] = "Test-developer-updated"
        self.user_attributes["role"] = User.Roles.ADMIN
        id = self.user_attributes["id"]
        response = self.update(key=id, data=self.user_attributes)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_another(self):
        another_user_attributes = {
            "username": "Test-manager",
            "name": "Test-manager",
            "surname": "Test-manager",
            "email": "test-manager@test.com",
            "password": "12345",
            "role": User.Roles.MANAGER,
        }
        user = self.create_api_user(another_user_attributes)
        id = user.id
        another_user_attributes["name"] = "Test-manager-updated"
        del another_user_attributes["password"]
        del another_user_attributes["role"]
        response = self.update(key=id, data=another_user_attributes)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_self(self):
        self.user_attributes["name"] = "Test-developer-updated"
        id = self.user_attributes["id"]
        del self.user_attributes["id"]
        del self.user_attributes["role"]
        response = self.update(key=id, data=self.user_attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        self.user_attributes["id"] = id
        assert response.json() == self.user_attributes
        self.user_attributes["role"] = "developer"

    def test_delete(self):
        response = self.delete(key=1)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content


class TestUserViewSetManager(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "Test-manager",
        "name": "Test-manager",
        "surname": "Test-manager",
        "email": "test-manager@test.com",
        "password": "12345",
        "role": User.Roles.MANAGER,
    }

    def test_list(self):
        response = self.list()
        assert response.status_code == HTTPStatus.OK, response.content
        del self.user_attributes["password"]
        self.user_attributes["role"] = "manager"
        expected_response = self.expected_details(
            response, self.user_attributes
        )
        assert response.json()[0] == expected_response
        self.user_attributes["id"] = expected_response["id"]

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])
        assert response.json() == self.user_attributes

    def test_update_role(self):
        self.user_attributes["name"] = "Test-manager-updated"
        self.user_attributes["role"] = User.Roles.ADMIN
        id = self.user_attributes["id"]
        response = self.update(key=id, data=self.user_attributes)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_self(self):
        self.user_attributes["name"] = "Test-manage-updated"
        id = self.user_attributes["id"]
        del self.user_attributes["id"]
        del self.user_attributes["role"]
        response = self.update(key=id, data=self.user_attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        self.user_attributes["id"] = id
        assert response.json() == self.user_attributes
        self.user_attributes["role"] = "manager"

    def test_update_another(self):
        another_user_attributes = {
            "username": "Test-developer",
            "name": "Test-developer",
            "surname": "Test-developer",
            "email": "test-developer@test.com",
            "password": "12345",
            "role": User.Roles.DEVELOPER,
        }
        user = self.create_api_user(another_user_attributes)
        id = user.id
        another_user_attributes["name"] = "Test-developer-updated"
        del another_user_attributes["password"]
        del another_user_attributes["role"]
        response = self.update(key=id, data=another_user_attributes)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_delete(self):
        response = self.delete(key=1)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content


class TestUserViewSetNonAutorized(TestViewSetBase):
    basename = "users"

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
