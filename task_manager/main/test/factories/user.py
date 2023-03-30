import factory
import random
from factory import Faker
from django.contrib.auth.hashers import make_password

from task_manager.main.models import User
from .base import ImageFileProvider


Faker.add_provider(ImageFileProvider)


class UserFactory(factory.Factory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("first_name")
    surname = Faker("last_name")
    role = random.choice(User.Roles.choices)[0]
    password = make_password("password")
    avatar_picture = Faker("image_file", fmt="jpeg")

    class Meta:
        model = dict
