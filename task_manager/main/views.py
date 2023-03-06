import django_filters
from rest_framework import viewsets
from django.db.models import Q


from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.prefetch_related("task_set").order_by("id")
    serializer_class = TagSerializer


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
        Task.objects
        .select_related("author", "executor")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
