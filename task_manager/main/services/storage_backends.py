from django.conf import settings
from django.core.files.storage import Storage
from django.utils.module_loading import import_string
from storages.backends.s3boto3 import S3Boto3Storage


class S3PublicStorage(S3Boto3Storage):  # pylint: disable=abstract-method
    default_acl = "public-read"
    querystring_auth = False


def public_storage() -> Storage:
    storage_path = getattr(
        settings, "PUBLIC_FILE_STORAGE", settings.DEFAULT_FILE_STORAGE
    )
    storage_class = import_string(storage_path)
    return storage_class()
