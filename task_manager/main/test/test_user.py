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
        "avatar_picture": None,
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_attributes["id"] = cls.user.id
        cls.user_attributes["role"] = "admin"
        del cls.user_attributes["password"]

    def test_create(self):
        response = self.create(data={})

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_list(self):
        user_2_attributes = {
            "username": "Test-admin-2",
            "name": "Test-admin",
            "surname": "Test-admin",
            "email": "test-admin@test.com",
            "password": "12345",
            "role": User.Roles.ADMIN,
            "avatar_picture": None,
        }
        user_2 = self.create_api_user(user_2_attributes)
        del user_2_attributes["password"]
        user_2_attributes["id"] = user_2.id

        response = self.list()
        expected_response = [self.user_attributes, user_2_attributes]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])

        assert response.json() == self.user_attributes

    def test_update(self):
        data = self.user_attributes.copy()
        data["username"] = "test-manager"
        data["password"] = "12345"
        data["role"] = User.Roles.MANAGER
        data["avatar_picture"] = ""
        del data["id"]
        another_user = self.create_api_user(data)

        response = self.update(
            key=another_user.id,
            data={"name": "Test-admin-updated", "role": "developer"},
        )

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

        response = self.update(key=another_user.id, data={"role": "developer"})

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == {"role": "developer"}

    def test_delete(self):
        another_user_attributes = {
            "username": "Test-manager",
            "name": "Test-manager",
            "surname": "Test-manager",
            "email": "test-manager@test.com",
            "password": "12345",
            "role": User.Roles.MANAGER,
            "avatar_picture": None,
        }
        another_user = self.create_api_user(another_user_attributes)
        id = another_user.id

        response = self.delete(key=id)
        response_list = self.list()
        expected_response_list = [self.user_attributes]

        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        assert response_list.json() == expected_response_list


class TestUserViewSetDeveloper(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
        "avatar_picture": None,
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_attributes["id"] = cls.user.id
        cls.user_attributes["role"] = "developer"
        del cls.user_attributes["password"]

    def test_list(self):
        user_2_attributes = {
            "username": "Test-admin-2",
            "name": "Test-admin",
            "surname": "Test-admin",
            "email": "test-admin@test.com",
            "password": "12345",
            "role": User.Roles.ADMIN,
            "avatar_picture": None,
        }
        user_2 = self.create_api_user(user_2_attributes)
        del user_2_attributes["password"]
        user_2_attributes["id"] = user_2.id

        response = self.list()
        expected_response = [self.user_attributes, user_2_attributes]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])

        assert response.json() == self.user_attributes

    def test_create(self):
        response = self.create(data={})

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_role(self):
        self.user_attributes["name"] = "Test-developer-updated"
        self.user_attributes["role"] = User.Roles.ADMIN
        self.user_attributes["avatar_picture"] = ""

        response = self.update(key=self.user.id, data=self.user_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_another(self):
        another_user_attributes = {
            "username": "Test-manager",
            "name": "Test-manager",
            "surname": "Test-manager",
            "email": "test-manager@test.com",
            "password": "12345",
            "role": User.Roles.MANAGER,
            "avatar_picture": None,
        }
        another_user = self.create_api_user(another_user_attributes)
        id = another_user.id
        another_user_attributes["name"] = "Test-manager-updated"
        another_user_attributes["avatar_picture"] = ""
        del another_user_attributes["password"]
        del another_user_attributes["role"]

        response = self.update(key=id, data=another_user_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_self(self):
        self.user_attributes["name"] = "Test-developer-updated"
        self.user_attributes["avatar_picture"] = ""
        id = self.user_attributes["id"]
        del self.user_attributes["id"]
        del self.user_attributes["role"]

        response = self.update(key=id, data=self.user_attributes)

        assert response.status_code == HTTPStatus.OK, response.content

        self.user_attributes["id"] = id
        self.user_attributes["avatar_picture"] = None

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
        "avatar_picture": None,
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_attributes["id"] = cls.user.id
        cls.user_attributes["role"] = "manager"
        del cls.user_attributes["password"]

    def test_list(self):
        user_2_attributes = {
            "username": "Test-admin-2",
            "name": "Test-admin",
            "surname": "Test-admin",
            "email": "test-admin@test.com",
            "password": "12345",
            "role": User.Roles.ADMIN,
            "avatar_picture": None,
        }
        user_2 = self.create_api_user(user_2_attributes)
        del user_2_attributes["password"]
        user_2_attributes["id"] = user_2.id

        response = self.list()
        expected_response = [self.user_attributes, user_2_attributes]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])

        assert response.json() == self.user_attributes

    def test_update_role(self):
        self.user_attributes["name"] = "Test-manager-updated"
        self.user_attributes["role"] = User.Roles.ADMIN
        self.user_attributes["avatar_picture"] = ""
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
        self.user_attributes["avatar_picture"] = None

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
            "avatar_picture": None,
        }
        another_user = self.create_api_user(another_user_attributes)
        id = another_user.id
        another_user_attributes["name"] = "Test-developer-updated"
        another_user_attributes["avatar_picture"] = ""
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
