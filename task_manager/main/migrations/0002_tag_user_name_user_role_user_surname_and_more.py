# Generated by Django 4.1.7 on 2023-03-01 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(default="Admin", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("developer", "Developer"),
                    ("manager", "Manager"),
                    ("admin", "Admin"),
                ],
                default="developer",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="surname",
            field=models.CharField(default="Admin", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254),
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("edited_at", models.DateField(auto_now_add=True)),
                ("deadline", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new task", "New Task"),
                            ("in development", "In Development"),
                            ("in qa", "In Qa"),
                            ("in code review", "In Code Review"),
                            ("ready for release", "Ready For Release"),
                            ("released", "Released"),
                            ("archived", "Archived"),
                        ],
                        default="new task",
                        max_length=255,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("high", "High"),
                            ("middle", "Middle"),
                            ("low", "Low"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="task_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "executor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="task_executor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("tags", models.ManyToManyField(to="main.tag")),
            ],
        ),
    ]