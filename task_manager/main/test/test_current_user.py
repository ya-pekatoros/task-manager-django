from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User
from task_manager.main.test.factories.user import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"
    user_attributes = UserFactory.build(role=User.Roles.ADMIN)

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUp()
        super().setUpTestData()

    def test_retrieve(self):
        user = self.single_resource()

        assert user == {
            "id": self.user.id,
            "email": self.user.email,
            "name": self.user.name,
            "surname": self.user.surname,
            "role": self.user.role.value,
            "username": self.user.username,
            "avatar_picture": "http://testserver" + self.user.avatar_picture.url,
        }

    def test_patch(self):
        self.patch_single_resource({"name": "TestName"})

        user = self.single_resource()
        assert user["name"] == "TestName"
