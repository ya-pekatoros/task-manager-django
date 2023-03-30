from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User
from http import HTTPStatus
from task_manager.main.test.factories.user import UserFactory
from django.core.files.uploadedfile import SimpleUploadedFile


class TestUserViewSetAdmin(TestViewSetBase):
    basename = "users"
    user_attributes = UserFactory.build(role=User.Roles.ADMIN)

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
        user_2_attributes = UserFactory.build()
        user_2 = self.create_api_user(user_2_attributes)
        del user_2_attributes["password"]
        user_2_attributes["id"] = user_2.id

        response = self.list()
        response_list = response.json()
        expected_response = [
            self.expected_details_user(response_list[0], self.user_attributes),
            self.expected_details_user(response_list[1], user_2_attributes),
        ]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_list == expected_response

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])
        response_dict = response.json()
        expected_response = self.expected_details_user(
            response_dict, self.user_attributes
        )

        assert response_dict == expected_response

    def test_update(self):
        another_user_attributes = UserFactory.build()
        another_user = self.create_api_user(another_user_attributes)

        response = self.update(
            key=another_user.id,
            data={"name": "Test-admin-updated", "role": "developer"},
        )

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

        response = self.update(key=another_user.id, data={"role": "developer"})

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == {"role": "developer"}

    def test_delete(self):
        another_user_attributes = UserFactory.build()
        another_user = self.create_api_user(another_user_attributes)
        id = another_user.id

        response = self.delete(key=id)
        response_list = self.list().json()
        expected_response_list = [
            self.expected_details_user(response_list[0], self.user_attributes)
        ]

        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        assert response_list == expected_response_list


class TestUserViewSetDeveloper(TestViewSetBase):
    basename = "users"
    user_attributes = UserFactory.build(role=User.Roles.DEVELOPER)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_attributes["id"] = cls.user.id
        cls.user_attributes["role"] = "developer"
        del cls.user_attributes["password"]

    def test_list(self):
        user_2_attributes = UserFactory.build()
        user_2 = self.create_api_user(user_2_attributes)
        del user_2_attributes["password"]
        user_2_attributes["id"] = user_2.id

        response = self.list()
        response_list = response.json()

        expected_response = [
            self.expected_details_user(response_list[0], self.user_attributes),
            self.expected_details_user(response_list[1], user_2_attributes),
        ]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_list == expected_response

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])
        response_dict = response.json()
        expected_response = self.expected_details_user(
            response_dict, self.user_attributes
        )

        assert response_dict == expected_response

    def test_create(self):
        response = self.create(data={})

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_role(self):
        self.user_attributes["role"] = User.Roles.ADMIN

        response = self.update(key=self.user.id, data=self.user_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_update_another(self):
        another_user_attributes = UserFactory.build()
        another_user = self.create_api_user(another_user_attributes)
        id = another_user.id
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
        self.user_attributes["avatar_picture"] = ""
        self.user_attributes["delete_avatar"] = False

        response = self.update(key=id, data=self.user_attributes)
        response_dict = response.json()

        del self.user_attributes["delete_avatar"]
        excepted_response = self.expected_details_user(
            response_dict, self.user_attributes
        )

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_dict == excepted_response

        self.user_attributes["role"] = "developer"

    def test_delete(self):
        response = self.delete(key=1)
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content


class TestUserViewSetManager(TestViewSetBase):
    basename = "users"
    user_attributes = UserFactory.build(role=User.Roles.MANAGER)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_attributes["id"] = cls.user.id
        cls.user_attributes["role"] = "manager"
        del cls.user_attributes["password"]

    def test_list(self):
        user_2_attributes = UserFactory.build()
        user_2 = self.create_api_user(user_2_attributes)
        del user_2_attributes["password"]
        user_2_attributes["id"] = user_2.id

        response = self.list()
        response_list = response.json()

        expected_response = [
            self.expected_details_user(response_list[0], self.user_attributes),
            self.expected_details_user(response_list[1], user_2_attributes),
        ]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_list == expected_response

    def test_retrieve(self):
        response = self.retrieve(key=self.user_attributes["id"])
        response_dict = response.json()
        expected_response = self.expected_details_user(
            response_dict, self.user_attributes
        )

        assert response_dict == expected_response

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
        response_dict = response.json()

        expected_response = self.expected_details_user(
            response_dict, self.user_attributes
        )

        assert response.status_code == HTTPStatus.OK, response.content
        assert response_dict == expected_response

        self.user_attributes["role"] = "manager"

    def test_update_another(self):
        another_user_attributes = UserFactory.build()
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


class TestUserViewSetAvatars(TestViewSetBase):
    basename = "users"
    user_attributes = UserFactory.build(role=User.Roles.DEVELOPER)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_attributes["id"] = cls.user.id
        cls.user_attributes["role"] = "developer"
        del cls.user_attributes["password"]

    def test_large_avatar(self) -> None:
        new_user_attr = self.user_attributes.copy()
        id = self.user_attributes["id"]
        del new_user_attr["id"]
        del new_user_attr["role"]
        user_new_avatar = UserFactory.build(
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
        )["avatar_picture"]
        new_user_attr["avatar_picture"] = user_new_avatar
        new_user_attr["delete_avatar"] = False

        response = self.update(key=id, data=new_user_attr)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        new_user_attr = self.user_attributes.copy()
        new_user_attr["avatar_picture"] = UserFactory.build()["avatar_picture"]
        id = self.user_attributes["id"]
        del new_user_attr["id"]
        del new_user_attr["role"]
        new_user_attr["avatar_picture"].name = "bad_extension.pdf"
        new_user_attr["delete_avatar"] = False

        response = self.update(key=id, data=new_user_attr)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
