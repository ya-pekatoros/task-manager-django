from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task, Tag


admin.site.register(User, UserAdmin)


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(User, site=task_manager_admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "surname", "email", "role")
    search_fields = ["username", "name", "surname", "email", "role"]


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author_name",
        "author_surname",
        "author_email",
        "executor_name",
        "executor_surname",
        "executor_email",
        "created_at",
        "edited_at",
        "deadline",
        "state",
        "priority",
        "display_tags",
    )
    search_fields = [
        "title",
        "author_name",
        "author_surname",
        "author_email",
        "executor_name",
        "executor_surname",
        "executor_email",
        "created_at",
        "edited_at",
        "deadline",
        "state",
        "priority",
        "display_tags",
    ]

    def author_name(self, obj):
        if obj.author:
            return obj.author.name

    def author_surname(self, obj):
        if obj.author:
            return obj.author.surname

    def author_email(self, obj):
        if obj.author:
            return obj.author.email

    def executor_name(self, obj):
        if obj.executor:
            return obj.executor.name

    def executor_surname(self, obj):
        if obj.executor:
            return obj.executor.surname

    def executor_email(self, obj):
        if obj.executor:
            return obj.executor.email

    def display_tags(self, obj):
        if obj.tags:
            return ", ".join([tag.title for tag in obj.tags.all()])
