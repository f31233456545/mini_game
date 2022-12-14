from django.contrib import admin

# Register your models here.
from room import models

class RoomAdmin(admin.ModelAdmin):
    # list_display: Sequence[Union[str, Callable[[_ModelT], Any]]]
    list_display = ['room_id', 'room_name', 'private', 'game_kind', 'creator_name', 'player_num', 'viewer_num', 'max_num', 'player_list_display', 'viewer_list_display']
admin.site.register(models.Room, RoomAdmin)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'password']
admin.site.register(models.UserInfo, UserInfoAdmin)