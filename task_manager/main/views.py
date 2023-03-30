import django_filters
from django.urls import reverse
from rest_framework import viewsets, mixins, status
from django.db.models import Q
from rest_framework import permissions
from typing import cast, Any
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import Http404, HttpResponse

from rest_framework_extensions.mixins import NestedViewSetMixin
from task_manager.main.services.single_resource import (
    SingleResourceMixin,
    SingleResourceUpdateMixin,
)
from .models import User, Task, Tag
from .serializers import (
    UserSerializer,
    UserSelfSerializer,
    UserAdminSerializer,
    UserSelfAdminSerializer,
    TaskSerializer,
    TaskPostSerializer,
    TaskPutExecutorSerializer,
    TaskPutAuthorSerializer,
    TaskPutAdminSerializer,
    TagSerializer,
    CountdownJobSerializer,
    JobSerializer,
)

from .permissions import TaskBase, UserBase, TagBase
from task_manager.main.services.async_celery import AsyncJob, JobStatus


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
                return UserSelfAdminSerializer
            if self.request.user.is_staff:
                return UserAdminSerializer
            if self.request.user == self.get_object():
                return UserSelfSerializer

        return UserSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        delete_avatar = serializer.validated_data.pop("delete_avatar", False)
        if delete_avatar:
            if user.avatar_picture:
                full_path = os.path.join(settings.MEDIA_ROOT, user.avatar_picture.name)
                if os.path.exists(full_path):
                    os.remove(full_path)
                user.avatar_picture.delete(save=False)

        serializer.save()
        return Response(serializer.data)


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
            if self.request.user == getattr(self.get_object(), "author"):
                return TaskPutAuthorSerializer
            if self.request.user.is_staff:
                return TaskPutAdminSerializer
            if self.request.user == getattr(self.get_object(), "executor"):
                return TaskPutExecutorSerializer

        return TaskSerializer


class TaskTagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    permission_classes = [permissions.IsAuthenticated, TagBase]

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "executor")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer

    filterset_class = TaskFilter
    permission_classes = [permissions.IsAuthenticated, TaskBase]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskPostSerializer
        if self.request.method in ["PUT", "PATCH"]:
            if self.request.user == getattr(self.get_object(), "author"):
                return TaskPutAuthorSerializer
            if self.request.user.is_staff:
                return TaskPutAdminSerializer
            if self.request.user == getattr(self.get_object(), "executor"):
                return TaskPutExecutorSerializer

        return TaskSerializer


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class CountdownJobViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CountdownJobSerializer

    def get_success_headers(self, data: dict) -> dict[str, str]:
        task_id = data["task_id"]
        return {"Location": reverse("jobs-detail", args=[task_id])}


class AsyncJobViewSet(viewsets.GenericViewSet):
    serializer_class = JobSerializer

    def get_object(self) -> AsyncJob:
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        task_id = self.kwargs[lookup_url_kwargs]
        job = AsyncJob.from_id(task_id)
        if job.status == JobStatus.UNKNOWN:
            raise Http404()
        return job

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data
        if instance.status == JobStatus.SUCCESS:
            location = self.request.build_absolute_uri(instance.result)
            return Response(
                serializer_data,
                headers={"location": location},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer_data)
