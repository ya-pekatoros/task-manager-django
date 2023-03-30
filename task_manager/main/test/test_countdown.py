import time
import pathlib
from http import HTTPStatus
import pytest
from django.test import override_settings
from django.urls import reverse

from task_manager.main.test.base import TestViewSetBase
from task_manager.main.models import User


class TestCountdownJob(TestViewSetBase):
    basename = "countdown"
    COUNTDOWN_TIME = 5
    user_attributes = {
        "username": "Test-developer",
        "name": "Test-developer",
        "surname": "Test-developer",
        "email": "test-developer@test.com",
        "password": "12345",
        "role": User.Roles.DEVELOPER,
    }

    @pytest.mark.slow
    def test_countdown_machinery(self):
        response = self.create({"seconds": self.COUNTDOWN_TIME})
        assert response.status_code == HTTPStatus.CREATED

        job_location = response.headers["Location"]
        start = time.monotonic()
        while response.data.get("status") != "success":
            assert time.monotonic() < start + self.COUNTDOWN_TIME + 1, "Time out"
            response = self.client.get(job_location)

        assert time.monotonic() > start + self.COUNTDOWN_TIME

        file_name = response.headers["Location"].split("/", 3)[-1]
        file = pathlib.Path(file_name)

        assert file.is_file()
        assert file.read_bytes() == b"test data"

        file.unlink(missing_ok=True)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_countdown(self):
        response = self.create({"seconds": 1})
        task_id = response.data["task_id"]
        file_name = f"{self.tmpdir}/test_report-{task_id}.data"
        file = pathlib.Path(file_name)
        assert file.is_file()
        assert file.read_bytes() == b"test data"
        file.unlink(missing_ok=True)
