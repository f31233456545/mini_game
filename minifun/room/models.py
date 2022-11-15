from email.policy import default
from tabnanny import verbose
from django.db import models
from minifun.desk import desk

#用户数据库
class UserInfo(models.Model):
    username = models.CharField(max_length=32, default="")
    password = models.CharField(max_length=32, default="")

    def __str__(self):
        return "Profile for user: username={0}, password={1}.\n".format(self.username, self.password)



class Room(models.Model):
    room_id = models.IntegerField()
    room_name = models.CharField(max_length = 128)
    private = models.BooleanField(default = False)    
    game_kind = models.IntegerField(default = 0)
    creator_name = models.CharField(max_length = 128)
    creator = models.ForeignKey(
        UserInfo, 
        on_delete=models.DO_NOTHING,
    )
    player_num = models.IntegerField(default = 0)
    viewer_num = models.IntegerField(default = 1)
    max_num = models.IntegerField(default = 13) # 8 players and 5 viewers.
    status = models.IntegerField(default = 0)
    player_list = models.ManyToManyField(
        UserInfo, 
        blank=True,
        related_name='player_list',
    )
    viewer_list = models.ManyToManyField(
        UserInfo, 
        blank=True,
        related_name='viewer_list',
    )
    desk = desk()

    def player_list_display(self):
        return ','.join([i.username for i in self.player_list.all()])
    
    def viewer_list_display(self):
        return ','.join([i.username for i in self.viewer_list.all()])
    
    def __str__(self):
        return "Profile for room {1}:\n    room_id={0}, private={2}, game_kind={3}\n    Created by user\n{4}    current player number={5}, viewer number={6}, maximal capacity={7}".format(
            self.room_id, self.room_name, self.private, self.game_kind, self.creator, self.player_num, self.viewer_num, self.max_num
        )
    