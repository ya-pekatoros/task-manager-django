from rest_framework import serializers

from .models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "name", "surname", "email", "role")


class UserSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "name", "surname", "email")


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("role",)


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    executor = UserSerializer(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True, slug_field="title", queryset=Tag.objects.all()
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "author",
            "executor",
            "description",
            "created_at",
            "edited_at",
            "deadline",
            "state",
            "priority",
            "tags",
        )


class TaskPostSerializer(serializers.ModelSerializer):
    executor = User.username
    tags = serializers.SlugRelatedField(
        many=True, slug_field="title", queryset=Tag.objects.all()
    )

    class Meta:
        model = Task
        fields = (
            "title",
            "executor",
            "description",
            "deadline",
            "priority",
            "tags",
        )

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        validated_data["state"] = Task.States.NEW
        return super().create(validated_data)


class TaskPutAuthorSerializer(serializers.ModelSerializer):
    executor = User.username
    tags = serializers.SlugRelatedField(
        many=True, slug_field="title", queryset=Tag.objects.all()
    )

    class Meta:
        model = Task
        fields = (
            "title",
            "executor",
            "description",
            "deadline",
            "priority",
            "state",
            "tags",
        )


class TaskPutExecutorSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, slug_field="title", queryset=Tag.objects.all()
    )

    class Meta:
        model = Task
        fields = ("state", "tags")


class TagSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source="task_set")

    class Meta:
        model = Tag
        fields = ("id", "title", "tasks")
