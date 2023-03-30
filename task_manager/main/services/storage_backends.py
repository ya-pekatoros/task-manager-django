import io

from django.conf import settings
from django.core.files.storage import Storage, default_storage
from django.utils.module_loading import import_string
from storages.backends.s3boto3 import S3Boto3Storage
from celery.app.task import Context


class S3PublicStorage(S3Boto3Storage):  # pylint: disable=abstract-method
    default_acl = "public-read"
    querystring_auth = False


def public_storage() -> Storage:
    storage_path = getattr(
        settings, "PUBLIC_FILE_STORAGE", settings.DEFAULT_FILE_STORAGE
    )
    storage_class = import_string(storage_path)
    return storage_class()


def local_file_name(report_name: str, request: Context, file_type: str) -> str:
    return f"{report_name}-{request.id}.{file_type}"


def save_file(file_name: str, report_file: io.BytesIO) -> str:
    file = default_storage.save(file_name, report_file)
    return default_storage.url(file)
