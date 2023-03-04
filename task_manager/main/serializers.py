from rest_framework import serializers

from .models import User, Task, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "name", "surname", "email", "role")


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    executor = UserSerializer(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )

    class Meta:
        model = Task
        fields = (
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


class TagSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source="task_set")

    class Meta:
        model = Tag
        fields = ("id", "title", "tasks")
