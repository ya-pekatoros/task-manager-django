from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task, Tag


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(User, site=task_manager_admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'email', 'role')
    search_fields = ['username', 'name', 'surname', 'email', 'role']


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    pass
