from task_manager.settings import *

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] += (
    "rest_framework.authentication.SessionAuthentication",
)
