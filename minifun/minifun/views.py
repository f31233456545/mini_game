from re import T
from django.http import HttpResponse
from django.shortcuts import render
import json
from room.models import Room
from room.admin import id_counter
from room import models
from room.models import UserInfo
# this is a test function.


def hello(request):
    return HttpResponse("Hello world ! ")


# this is a test function.
def template(request):
    views_dict = {"name": "菜鸟教程"}
    return render(request, "views_dict.html", {"views_dict": views_dict})

# login function


def login(request):
    if request.method == "GET":

        # get param 'username'
        u = request.GET.get("username")
        # get param 'password'
        p = request.GET.get("password")

        x = models.UserInfo.objects.filter(username=u)[0]
        if x:
            if x.password == p:
                # create a python dictionary
                resp = {}
                resp['message'] = "登陆成功"
                resp['succeed'] = True
                # convert dict to json
                return HttpResponse(json.dumps(resp))
                return HttpResponse("登录成功")
            else:
                resp = {}
                resp['message'] = "密码错误"
                resp['succeed'] = False
                # convert dict to json
                return HttpResponse(json.dumps(resp))
                return HttpResponse("密码错误")
        else:
            # create a python dictionary
            resp = {}
            resp['message'] = "用户名不存在"
            resp['succeed'] = False
            # convert dict to json
            return HttpResponse(json.dumps(resp))
            return HttpResponse("用户名不存在")


# register function


def register(request):
    if request.method == "GET":

        # get param 'username'
        u = request.GET.get("username")
        # get param 'password'
        p = request.GET.get("password")

        # 检查数据库中是否存在该用户名
        x = models.UserInfo.objects.filter(username=u)[0]

        if x:
            # 存在
            
            
            resp = {}
            resp['message'] = "用户名已存在"
            resp['succeed'] = False
            # convert dict to json
            return HttpResponse(json.dumps(resp))
            return HttpResponse("注册成功")

        else:
            # 不存在
            # 定义数据库表userinfo对象
            user = models.UserInfo()
            user.username = u
            user.password = p
            # 将数据写入数据库
            user.save()
            resp = {}
            resp['message'] = "注册成功"
            resp['succeed'] = True
            # convert dict to json
            return HttpResponse(json.dumps(resp))
            return HttpResponse("用户名已存在")


# create a room function


def create_room(request):
    # Note: After the creator creates the room, he needs manually send a join_room request to join the room.
    # TODO: should we auto join_room after create_room?
    global id_counter
    # default: 0, that is a public room
    my_private = request.GET.get("private")
    my_room_name = request.GET.get("room_name")
    # default: Texas Hold'em poker
    my_game_kind = request.GET.get("game_kind")
    my_creator_name = request.GET.get("creator_name")
    my_max_num_int = 13     # default: 8 players and 5 viewers at most.
    # TODO: self-defined capacity of the room?
    # my_max_num = request.GET.get("max_num")
    # if not my_max_num:
    #     my_max_num = '13'
    # my_max_num_int = int(my_game_kind)

    resp = {}
    if ((not my_room_name) or (not my_creator_name)):
        resp['succeed'] = False
        resp['room_id'] = -1
        resp['message'] = "Require room name and username of the creator."
        return HttpResponse(json.dumps(resp))
    # TODO: check if the creator is a valid account by filtering in database of USERINFO
    # usr = UserInfo.objects.get(username=my_creator_name)
    # if not usr:
    #    resp['succeed'] = False
    #    resp['room_id'] = -1
    #    resp['message'] = "Invalid username of the creator."
    #    return HttpResponse(json.dumps(resp))

    r = Room.objects.filter(room_name=my_room_name)
    if r:
        resp['succeed'] = False
        resp['room_id'] = -1
        resp['message'] = "Room "+my_room_name+" already exists."
        return HttpResponse(json.dumps(resp))

    if not my_private:
        my_private = '1'
    my_private_bl = bool(my_private)
    if not my_game_kind:
        my_game_kind = '0'
    my_game_kind_int = int(my_game_kind)
    id_counter = 1
    for r in Room.objects.all():
        if r.room_id == id_counter:    
            id_counter = r.room_id+1
    r = Room(room_id=id_counter, room_name = my_room_name, private=my_private_bl,
             game_kind=my_game_kind_int, creator_name=my_creator_name,
             player_num=0, viewer_num=0, max_num=my_max_num_int)
    # r.creator = usr
    r.save()
    resp['succeed'] = True
    resp['room_id'] = id_counter
    resp['message'] = "success"
    # debug
    # Print the database
    print(Room.objects.all())
    return HttpResponse(json.dumps(resp))


def join_room(request):
    my_room_id = request.GET.get("room_id")
    my_username = request.GET.get("user_name")

    resp = {}
    if (not my_room_id) or (not my_username):
        resp['succeed'] = False
        resp['message'] = "Invalid room id or username."
        return HttpResponse(json.dumps(resp))
    # TODO: check if the user is a valid account by filtering in database of USERINFO
    # usr = UserInfo.objects.get(username=my_username)
    # if not usr:
    #    resp['succeed'] = False
    #    resp['message'] = "Invalid username."
    #    return HttpResponse(json.dumps(resp))
    my_room_id_int = int(my_room_id)
    rs = Room.objects.filter(room_id=my_room_id_int)
    if rs:
        r = rs[0]
    else:
        resp['succeed'] = False
        resp['message'] = "Room "+my_room_id+" does not exist."
        return HttpResponse(json.dumps(resp))
    
    if not r:
        resp['succeed'] = False
        resp['message'] = "Room "+my_room_id+" does not exist."
        return HttpResponse(json.dumps(resp))
    if r.player_num+r.viewer_num > r.max_num:
        resp['succeed'] = False
        resp['message'] = "Room "+my_room_id+" is filled to capacity."
        return HttpResponse(json.dumps(resp))
    # TODO: check if the user is already in the room
    # TODO: a conception: blacklist?
    #tmp_usr = r.viewer_list.get(username=my_username)
    # if tmp_usr:
    #    resp['succeed'] = False
    #    resp['message'] = "User "+my_username+" is already in room "+my_room_id+"."
    #    return HttpResponse(json.dumps(resp))
    r.viewer_num = r.viewer_num+1
    # TODO: add the user into viewer list
    # r.viewer_list.add(usr)
    r.save()
    resp['succeed'] = True
    resp['message'] = "Welcome to room " + my_room_id
    # debug
    # Print the database
    for r in Room.objects.all():
        print(r)
        # TODO: print the ForeignKey and ManyToManyField
        # print(r.creator)
        # for player in r.player_list.all():
        #   print(player)
        # for viewer in r.player_list.all():
        #   print(viewer)
    return HttpResponse(json.dumps(resp))


def exit_room(request):
    my_room_id = request.GET.get("room_id")
    my_username = request.GET.get("user_name")

    resp = {}
    if (not my_room_id) or (not my_username):
        resp['succeed'] = False
        resp['message'] = "Invalid room id or username."
        return HttpResponse(json.dumps(resp))
    # TODO: check if the user is a valid account by filtering in database of USERINFO
    # usr = UserInfo.objects.get(username=my_username)
    # if not usr:
    #    resp['succeed'] = False
    #    resp['message'] = "Invalid username."
    #    return HttpResponse(json.dumps(resp))
    my_room_id_int = int(my_room_id)
    rs = Room.objects.filter(room_id=my_room_id_int)
    if rs:
        r = rs[0]
    else:
        resp['succeed'] = False
        resp['message'] = "Room "+my_room_id+" does not exist."
        return HttpResponse(json.dumps(resp))
        
    if not r:
        resp['succeed'] = False
        resp['message'] = "Room "+my_room_id+" does not exist."
        return HttpResponse(json.dumps(resp))
    # TODO: check if the user is in the room
    # TODO: a viewer or a player?
    if r.viewer_num == 0:
        resp['succeed'] = False
        resp['message'] = "User "+my_username+" is not in room "+my_room_id+"."
        return HttpResponse(json.dumps(resp))
    #tmp_usr = r.viewer_list.get(username=my_username)
    # if !tmp_usr:
    #    resp['succeed'] = False
    #    resp['message'] = "User "+my_username+" is not in room "+my_room_id+"."
    #    return HttpResponse(json.dumps(resp))
    # TODO: transfer the host to someone else?
    #if my_username == r.creator_name:
    #      
    r.viewer_num = r.viewer_num-1
    # TODO: add the user into viewer list
    # r.viewer_list.add(usr)
    r.save()
    resp['succeed'] = True
    resp['message'] = "Goodbye from room " + my_room_id
    # debug
    # Print the database
    for r in Room.objects.all():
        print(r)
        # TODO: print the ForeignKey and ManyToManyField
        # print(r.creator)
        # for player in r.player_list.all():
        #   print(player)
        # for viewer in r.player_list.all():
        #   print(viewer)
    return HttpResponse(json.dumps(resp))


def request_room_list(request):
    my_game_kind = request.GET.get("game_kind")
    my_user_name = request.GET.get("user_name")

    resp = {}
    r = Room.objects.filter(game_kind=my_game_kind)
    if not r:
        resp['rooms'] = []
        return HttpResponse(json.dumps(resp))
    rooms = []
    for r in Room.objects.filter(game_kind=my_game_kind):
        room = {'room_id': r.room_id, 'game_kind': r.game_kind, 'room_name': r.room_name,
                'player_num': r.player_num, 'viewer_num': r.viewer_num, 'max_num': r.max_num, 'status': r.status}
        rooms.append(room)
    resp['rooms'] = rooms
    for r in Room.objects.filter(game_kind=my_game_kind):
        print(r)

    return HttpResponse(json.dumps(resp))
