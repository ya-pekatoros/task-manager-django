from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task, Tag

<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
admin.site.register(User, UserAdmin)
=======
>>>>>>> Stashed changes

class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(User, site=task_manager_admin_site)
class UserAdmin(admin.ModelAdmin):
<<<<<<< Updated upstream
    list_display = ('username', 'name', 'surname', 'email', 'role')
    search_fields = ['username', 'name', 'surname', 'email', 'role']
=======
    list_display = ("username", "name", "surname", "email", "role")
    search_fields = ["username", "name", "surname", "email", "role"]
>>>>>>> Stashed changes


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
<<<<<<< Updated upstream
    pass
=======
    list_display = (
        "title", "author_name", "author_surname", "author_email",
        "executor_name", "executor_surname", "executor_email", "created_at",
        "edited_at", "deadline", "state", "priority", "display_tags"
    )
    search_fields = [
        "title", "author_name", "author_surname", "author_email",
        "executor_name", "executor_surname", "executor_email", "created_at",
        "edited_at", "deadline", "state", "priority", "display_tags"
    ]

    def author_name(self, obj):
        return obj.author.name

    def author_surname(self, obj):
        return obj.author.surname

    def author_email(self, obj):
        return obj.author.email

    def executor_name(self, obj):
        return obj.executor.name

    def executor_surname(self, obj):
        return obj.executor.surname

    def executor_email(self, obj):
        return obj.executor.email

    def display_tags(self, obj):
        return ", ".join([tag.title for tag in obj.tags.all()])
>>>>>>> Stashed changes
>>>>>>> Stashed changes
