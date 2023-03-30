from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User
from http import HTTPStatus


class TestTagViewSetNonAutorized(TestViewSetBase):
    basename = "tags"

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

    def test_create(self):
        tag_attributes = {"title": "bug"}

        response = self.create(data=tag_attributes)
        response_dict = response.json()

        tag_attributes["tasks"] = []
        expected_response = self.expected_details(response_dict, tag_attributes)

        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response_dict == expected_response

    def test_list(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)
        tag_2_attributes = {"title": "bug"}
        tag_2 = self.create_tag(tag_2_attributes)

        response = self.list()
        expected_response = [self.get_expected_tag_attr(tag), self.get_expected_tag_attr(tag_2)]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        response = self.retrieve(key=tag.id)

        expected_response = self.get_expected_tag_attr(tag)

        assert response.json() == expected_response

    def test_update(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        tag_attributes["tasks"] = []
        tag_attributes["title"] = "bug-updated"

        response = self.update(key=tag.id, data=tag_attributes)
        response_dict = response.json()

        assert response.status_code == HTTPStatus.OK, response.content

        expected_response = self.expected_details(response_dict, tag_attributes)

        assert response_dict == expected_response

    def test_delete(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        tag_2_attributes = {"title": "bug"}
        tag_2 = self.create_tag(tag_2_attributes)

        response = self.delete(key=tag.id)
        response_list = self.list()
        expected_response_list = [self.get_expected_tag_attr(tag_2)]

        assert response_list.json() == expected_response_list
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content


class TestTagViewSetDeveloper(TestViewSetBase):
    basename = "tags"
    user_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
    }

    def test_create(self):
        tag_attributes = {"title": "bug"}

        response = self.create(data=tag_attributes)
        response_dict = response.json()

        tag_attributes["tasks"] = []

        expected_response = self.expected_details(response_dict, tag_attributes)

        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response_dict == expected_response

    def test_list(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        tag_2_attributes = {"title": "bug"}
        tag_2 = self.create_tag(tag_2_attributes)

        response = self.list()
        expected_response = [self.get_expected_tag_attr(tag), self.get_expected_tag_attr(tag_2)]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        response = self.retrieve(key=tag.id)

        expected_response = self.get_expected_tag_attr(tag)

        assert response.json() == expected_response

    def test_update(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        tag_attributes["tasks"] = []
        tag_attributes["title"] = "bug-updated"

        response = self.update(key=tag.id, data=tag_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_delete(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        response = self.delete(key=tag.id)

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
        tag_attributes = {"title": "bug"}

        response = self.create(data=tag_attributes)
        response_dict = response.json()

        tag_attributes["tasks"] = []
        expected_response = self.expected_details(response_dict, tag_attributes)

        assert response.status_code == HTTPStatus.CREATED, response.content
        assert response_dict == expected_response

    def test_list(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        tag_2_attributes = {"title": "bug"}
        tag_2 = self.create_tag(tag_2_attributes)

        response = self.list()
        expected_response = [self.get_expected_tag_attr(tag), self.get_expected_tag_attr(tag_2)]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)
        tag_attributes["tasks"] = []

        response = self.retrieve(key=tag.id)

        expected_response = self.get_expected_tag_attr(tag)

        assert response.json() == expected_response

    def test_update(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        tag_attributes["tasks"] = []
        tag_attributes["title"] = "bug-updated"

        response = self.update(key=tag.id, data=tag_attributes)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content

    def test_delete(self):
        tag_attributes = {"title": "bug"}
        tag = self.create_tag(tag_attributes)

        response = self.delete(key=tag.id)

        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
