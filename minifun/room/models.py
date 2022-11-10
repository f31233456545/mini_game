from email.policy import default
from tabnanny import verbose
from django.db import models

# Create your models here.
class Room(models.Model):
    room_id = models.IntegerField()
    room_name = models.CharField(max_length = 128)
    private = models.BooleanField(default = False)    
    game_kind = models.IntegerField(default = 0)
    creator_name = models.CharField(max_length = 128)
    # TODO: can be defined as a foreignkey to a user class member
    # creator = models.ForeignKey(
    #    UserInfo, 
    #    on_delete=models.CASCADE
    #)
    player_num = models.IntegerField(default = 0)
    viewer_num = models.IntegerField(default = 1)
    max_num = models.IntegerField(default = 13) # 8 players and 5 viewers.
    status = models.IntegerField(default = 0)

    # TODO: Foreignkey lists of current players and viewers.
    # player_list = models.ManyToManyField(
    #    UserInfo, 
    #    on_delete=models.CASCADE
    #)
    # viewer_list = models.ManyToManyField(
    #    UserInfo, 
    #    on_delete=models.CASCADE
    #)
    def __str__(self):
        return "Profile for room {1}:\n    room_id={0}, private={2}, game_kind={3}\n    Created by user {4}\n    current player number={5}, viewer number={6}, maximal capacity={7}".format(
            self.room_id, self.room_name, self.private, self.game_kind, self.creator_name, self.player_num, self.viewer_num, self.max_num
        )
    # TODO: Foreignkey lists of current players and viewers.
    #def creator_dis(self):
    #    return str(self.creator.username) 
    #def player_list_dis(self):
    #    return ','.join([i.username for i in self.player_list.all()])
    #def viewer_list_dis(self):
    #    return ','.join([i.username for i in self.viewer_list.all()])
    
#用户数据库
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)