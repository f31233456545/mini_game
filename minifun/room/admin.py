from django.contrib import admin

# Register your models here.
from room import models

class RoomAdmin(admin.ModelAdmin):
    # list_display: Sequence[Union[str, Callable[[_ModelT], Any]]]
    list_display = ['room_id', 'room_name', 'private', 'game_kind', 'creator_name', 'player_num', 'viewer_num', 'max_num']
    # TODO: with ForeignKey and ManyToManyField
    # list_display = ['room_id', 'room_name', 'private', 'game_kind', 'creator_dis', 'player_num', 'player_list_dis', 'viewer_num', 'viewer_list_dis', 'max_num']
admin.site.register(models.Room, RoomAdmin)
id_counter = 0  # the maximal id of the created rooms, increment and then use each time you create a room.
