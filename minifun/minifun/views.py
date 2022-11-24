from re import T
from django.http import HttpResponse
from django.shortcuts import render
import json
from room.models import Room
from room import models
from room.models import UserInfo
from .desk import desk, desks
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

        x = models.UserInfo.objects.filter(username=u)
        if x:
            if x[0].password == p:
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
        x = models.UserInfo.objects.filter(username=u)

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
    my_private = request.GET.get("private")
    my_room_name = request.GET.get("room_name")
    my_game_kind = request.GET.get("game_kind")
    my_creator_name = request.GET.get("creator_name")
    my_max_num_int = 13
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
    usrs = UserInfo.objects.filter(username=my_creator_name)
    if usrs:
        usr = usrs[0]
    else:
        resp['succeed'] = False
        resp['room_id'] = -1
        resp['message'] = "Invalid username of the creator."
        return HttpResponse(json.dumps(resp))
    my_private_bl = True
    if my_private == '0' or my_private == 'false' or my_private=='False':
        my_private_bl = False
    # print(my_private)
    if not my_game_kind:
        my_game_kind = '0'
    my_game_kind_int = int(my_game_kind)
    id_counter = 0
    for r in Room.objects.all():
        if r.room_id > id_counter:
            id_counter = r.room_id
    id_counter = id_counter+1
    r = Room(room_id=id_counter, room_name = my_room_name, private=my_private_bl,
             game_kind=my_game_kind_int, creator_name=my_creator_name, creator=usr, 
             player_num=0, viewer_num=0, max_num=my_max_num_int)
    d = desk()
    desks[r.room_id] = d
    desks[r.room_id].create_room(r.private, r.room_name, r.game_kind, r.creator_name)
    r.save()
    resp['succeed'] = True
    resp['room_id'] = id_counter
    resp['message'] = "success"
    # debug
    print(Room.objects.all())
    print(desks)
    return HttpResponse(json.dumps(resp))
