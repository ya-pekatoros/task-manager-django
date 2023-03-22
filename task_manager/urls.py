"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_extensions.routers import ExtendedSimpleRouter
from django.conf.urls.static import static
from django.conf import settings

from task_manager.main.admin import task_manager_admin_site
from task_manager.main.services.single_resource import BulkRouter
from task_manager.main.views import (
    UserViewSet,
    TaskViewSet,
    TagViewSet,
    CurrentUserViewSet,
    UserTasksViewSet,
    TaskTagsViewSet,
    CountdownJobViewSet,
    AsyncJobViewSet
)


router = ExtendedSimpleRouter()
router.register(r"users", UserViewSet, basename="users").register(
    r"tasks",
    UserTasksViewSet,
    basename="user_tasks",
    parents_query_lookups=["executor_id"],
)
router.register(r"tasks", TaskViewSet, basename="tasks").register(
    r"tags",
    TaskTagsViewSet,
    basename="task_tags",
    parents_query_lookups=["task_id"],
)

router.register(r"tags", TagViewSet, basename="tags")

router.register(r"countdown", CountdownJobViewSet, basename="countdown")

router.register(r"jobs", AsyncJobViewSet, basename="jobs")

bulk_router = BulkRouter()
bulk_router.register(r"current-user", CurrentUserViewSet, basename="current_user")


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
    path("api/", include(router.urls)),
    path("api/", include(bulk_router.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
