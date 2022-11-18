from django.apps import AppConfig


class RoomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "room"

class UserInfoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "userinfo"
