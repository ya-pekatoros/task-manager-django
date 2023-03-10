import django_filters
from rest_framework import viewsets
from django.db.models import Q
from rest_framework import permissions


from .models import User, Task, Tag
from .serializers import (
    UserSerializer,
    UserSelfSerializer,
    UserAdminSerializer,
    TaskSerializer,
    TaskPostSerializer,
    TaskPutExecutorSerializer,
    TaskPutAuthorSerializer,
    TagSerializer,
)

from .permissions import TaskBase, UserBase, TagBase


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    filterset_class = UserFilter
    permission_classes = [permissions.IsAuthenticated, UserBase]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            if self.request.user == self.get_object() and self.request.user.is_staff:
                return UserSerializer
            if self.request.user.is_staff:
                return UserAdminSerializer
            if self.request.user == self.get_object():
                return UserSelfSerializer

        return UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.prefetch_related("task_set").order_by("id")
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, TagBase]


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(field_name="state", lookup_expr="iexact")
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__title",
        to_field_name="title",
        queryset=Tag.objects.all(),
    )
    author = django_filters.CharFilter(
        method="filter_author", label="Author name, surname or email"
    )
    executor = django_filters.CharFilter(
        method="filter_executor", label="Executor name, surname or email"
    )

    class Meta:
        model = Task
        fields = ["state", "tags", "author", "executor"]

    def filter_author(self, queryset, _, value):
        return queryset.filter(
            Q(author__name__icontains=value)
            | Q(author__surname__icontains=value)
            | Q(author__email__icontains=value)
        )

    def filter_executor(self, queryset, _, value):
        return queryset.filter(
            Q(executor__name__icontains=value)
            | Q(executor__surname__icontains=value)
            | Q(executor__email__icontains=value)
        )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "executor")
        .prefetch_related("tags")
        .order_by("id")
    )

    filterset_class = TaskFilter
    permission_classes = [permissions.IsAuthenticated, TaskBase]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskPostSerializer
        if self.request.method in ["PUT", "PATCH"]:
            if (
                self.request.user == getattr(self.get_object(), "author")
                or self.request.user.is_staff
            ):
                return TaskPutAuthorSerializer
            if self.request.user == getattr(self.get_object(), "executor"):
                return TaskPutExecutorSerializer

        return TaskSerializer
