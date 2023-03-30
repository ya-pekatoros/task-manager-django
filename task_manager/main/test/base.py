from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from typing import Union, List, Dict
from rest_framework.response import Response
import tempfile
import os
from django.conf import settings
from http import HTTPStatus
import datetime

from task_manager.main.models import User, Task, Tag


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    user_attributes: Dict[str, Union[str, int, List[int]]] = None
    today: datetime.date

    @classmethod
    def setUp(cls):
        cls.tmpdir = tempfile.mkdtemp()
        settings.MEDIA_URL = cls.tmpdir
        settings.MEDIA_ROOT = cls.tmpdir

    @classmethod
    def tearDown(cls):
        for filename in os.listdir(cls.tmpdir):
            file_path = os.path.join(cls.tmpdir, filename)
            os.remove(file_path)

        os.rmdir(cls.tmpdir)

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        if cls.user_attributes:
            cls.user = cls.create_api_user(cls.user_attributes)
        else:
            cls.user = None
        cls.client = APIClient()

    @staticmethod
    def create_api_user(user_attributes):
        return User.objects.create(**user_attributes)

    @staticmethod
    def create_task(task_attributes):
        return Task.objects.create(**task_attributes)

    @staticmethod
    def create_tag(tag_attributes):
        return Tag.objects.create(**tag_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @staticmethod
    def expected_details(entity: bytes, attributes: dict):
        return {**attributes, "id": entity["id"]}

    @staticmethod
    def expected_details_user(entity: bytes, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    @staticmethod
    def login(client, user):
        return client.force_login(user)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.login(self.client, self.user)
        response = self.client.post(self.list_url(args), data=data)
        return response

    def list(self, args: List[Union[str, int]] = None) -> dict:
        self.login(self.client, self.user)
        response = self.client.get(self.list_url(args))
        return response

    def retrieve(self, key: Union[int, str]) -> dict:
        self.login(self.client, self.user)
        response = self.client.get(self.detail_url(key))
        return response

    def update(self, key: Union[int, str], data: dict) -> dict:
        self.login(self.client, self.user)
        response = self.client.put(self.detail_url(key), data=data)
        return response

    def delete(self, key: Union[int, str]) -> None:
        self.login(self.client, self.user)
        response = self.client.delete(self.detail_url(key))
        return response

    def request_single_resource(self, data: dict = None) -> Response:
        self.login(self.client, self.user)
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        self.login(self.client, self.user)
        url = self.list_url()
        return self.client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
    
    @classmethod
    def get_expected_task_attr(cls, task: Task) -> dict:
        tag_list = [tag.title for tag in task.tags.all()]
        expected_task_attr = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "deadline": task.deadline if isinstance(task.deadline, str) else task.deadline.strftime('%Y-%m-%d'),
            "author": {
                "id": task.author.id,
                "username": task.author.username,
                "email": task.author.email,
                "name": task.author.name,
                "surname": task.author.surname,
                "role": task.author.role,
                "avatar_picture": (
                    "http://testserver" + task.author.avatar_picture.url if task.author.avatar_picture else None
                ),
            },
            "executor": {
                "id": task.executor.id,
                "username": task.executor.username,
                "email": task.executor.email,
                "name": task.executor.name,
                "surname": task.executor.surname,
                "role": task.executor.role,
                "avatar_picture": (
                    "http://testserver" + task.executor.avatar_picture.url if task.author.avatar_picture else None
                ),
            },
            "created_at": cls.today,
            "edited_at": cls.today,
            "tags": tag_list,
            "state": task.state,
            "priority": task.priority,
        }
        return expected_task_attr

    @classmethod
    def get_expected_tag_attr(cls, tag: Tag) -> dict:
        task_list = [cls.get_expected_task_attr(task) for task in tag.task_set.all()]
        return {
            "id": tag.id,
            "title": tag.title,
            "tasks": task_list
        }
