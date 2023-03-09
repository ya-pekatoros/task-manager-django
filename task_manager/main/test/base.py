from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from typing import Union, List, Dict
from factory.django import DjangoModelFactory
from factory import Faker
from django.contrib.auth.hashers import make_password

from task_manager.main.models import User, Task, Tag


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    user_attributes: Dict[str, Union[str, int, List[int]]] = None

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
        entity_decoded = entity.json()
        if isinstance(entity_decoded, list):
            entity_decoded = entity_decoded[0]
        return {**attributes, "id": entity_decoded["id"]}

    @staticmethod
    def login(client, user):
        return client.force_login(user)

    # def find_(self, parameter, value, dictionary):
    #     if parameter in dictionary:
    #         if dictionary[parameter] == value:
    #             return True
    #     for key in dictionary:
    #         if isinstance(dictionary[key], dict):
    #             result = self.find_key(parameter, value, dictionary[key])
    #             if result:
    #                 return True
    #     return False

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

class UserFactory(DjangoModelFactory):
    username = Faker('user_name')
    email = Faker('email')
    password = make_password('password')

    class Meta:
        model = User
