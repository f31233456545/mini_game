from re import T
from django.http import HttpResponse
from django.shortcuts import render
import json
from room.models import Room
from room import models
from room.models import UserInfo
from .desk import desks,desk
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
    # print(Room.objects.all())
    print(desks)
    return HttpResponse(json.dumps(resp))

def join_room(request):
    my_room_id = request.GET.get("room_id")
    my_username = request.GET.get("user_name")

    resp = {}
    if (not my_room_id) or (not my_username):
        resp['succeed'] = False
        resp['message'] = "Invalid room id or username."
        return HttpResponse(json.dumps(resp))
    usrs = UserInfo.objects.filter(username=my_username)
    if not usrs:
        resp['succeed'] = False
        resp['message'] = "Invalid username."
        return HttpResponse(json.dumps(resp))
    else:
        usr = usrs[0]
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
    # TODO: a conception: blacklist?
    vusrs = r.viewer_list.filter(username=my_username)
    if vusrs:
        resp['succeed'] = False
        resp['message'] = "User "+my_username+" is already in room "+my_room_id+"."
        return HttpResponse(json.dumps(resp))
    pusrs = r.player_list.filter(username=my_username)
    if pusrs:
        resp['succeed'] = False
        resp['message'] = "User "+my_username+" is already in room "+my_room_id+"."
        return HttpResponse(json.dumps(resp))
    r.viewer_num = r.viewer_num+1
    r.viewer_list.add(usr)
    r.save()
    resp['succeed'] = True
    resp['message'] = "Welcome to room " + my_room_id
    # debug
    for r in Room.objects.all():
        print(r)
    return HttpResponse(json.dumps(resp))


def exit_room(request):
    my_room_id = request.GET.get("room_id")
    my_username = request.GET.get("user_name")

    resp = {}
    if (not my_room_id) or (not my_username):
        resp['succeed'] = False
        resp['message'] = "Invalid room id or username."
        return HttpResponse(json.dumps(resp))
    usrs = UserInfo.objects.filter(username=my_username)
    if not usrs:
        resp['succeed'] = False
        resp['message'] = "Invalid username."
        return HttpResponse(json.dumps(resp))
    else:
        usr = usrs[0]
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
    pusrs = r.player_list.filter(username=my_username)
    if pusrs:
        if desks[r.room_id].stand(my_room_id, my_username):
            r.player_num -= 1
            r.viewer_num += 1
            r.player_list.remove(pusrs[0])
            r.viewer_list.add(pusrs[0])
            r.save()
        resp['succeed'] = True
        resp['message'] = "Goodbye from room " + my_room_id
        return HttpResponse(json.dumps(resp))
    vusrs = r.viewer_list.filter(username=my_username)
    if not vusrs:
        resp['succeed'] = False
        resp['message'] = "User "+my_username+" is not in room "+my_room_id+"."
        return HttpResponse(json.dumps(resp))
    r.viewer_list.remove(vusrs[0])
    # TODO: transfer the host to someone else?
    r.viewer_num = r.viewer_num-1
    r.save()
    if r.viewer_num+r.player_num == 0:
        r.delete()
    resp['succeed'] = True
    resp['message'] = "Goodbye from room " + my_room_id
    # debug
    for r in Room.objects.all():
        print(r)
    return HttpResponse(json.dumps(resp))


def sit(request):
    my_room_id = request.GET.get("room_id")
    my_user_name = request.GET.get("user_name")
    my_chip_cnt = request.GET.get("chip_cnt")

    resp={}
    #seat_id = -1 when failing to sit

    #room doesn't exist
    if not Room.objects.filter(room_id=my_room_id):
        resp['succeed'] = False
        resp['message'] = "Room "+str(my_room_id)+" does not exist."
        resp['seat_id'] = -1
        return HttpResponse(json.dumps(resp))
    room = Room.objects.filter(room_id=my_room_id)[0]
    #player_num has reached to maximum
    if room.player_num == 8:
        resp['succeed'] = False
        resp['message'] = " seat for player are full. "
        resp['seat_id'] = -1
        return HttpResponse(json.dumps(resp))
    vusrs = room.viewer_list.filter(username=my_user_name)
    if not vusrs:
        resp['succeed'] = False
        resp['message'] = "User "+my_user_name+" is not a viewer in room "+str(my_room_id)+"."
        resp['seat_id'] = -1
        return HttpResponse(json.dumps(resp))
    
    #modify desk.user_info and assign right seat_id(by calling room.desk.sit)
    #distribute seat for player 
    resp['succeed'] = True
    resp['message'] = "assign minimum available seat_id."
    
    # default value of chip cnt
    stack_cnt=0
    if not my_chip_cnt:
        stack_cnt=200
    else:
        stack_cnt=int(my_chip_cnt)
    resp['seat_id'] = desks[room.room_id].sit(my_room_id,my_user_name,stack_cnt)

    #modified database message of room
    room.player_num += 1
    room.viewer_num -= 1
    room.viewer_list.remove(vusrs[0])
    room.player_list.add(vusrs[0])
    room.save()
    return HttpResponse(json.dumps(resp))

def stand(request):
    my_room_id = int(request.GET.get("room_id"))
    my_user_name = request.GET.get("user_name")
    
    resp = {}
    #room don't exist
    if not Room.objects.filter(room_id=my_room_id):
        resp['succeed'] = False
        resp['message'] = "Room "+str(my_room_id)+" does not exist."
        return HttpResponse(json.dumps(resp))

    room = Room.objects.filter(room_id=my_room_id)[0]
    pusrs = room.player_list.filter(username=my_user_name)
    if not pusrs:
        resp['succeed'] = False
        resp['message'] = "User "+my_user_name+" is not a player in room "+str(my_room_id)+"."
        return HttpResponse(json.dumps(resp))
    #judge if user_name is valid(by calling stand)
    #modify desk.user_info and database message of room
    if desks[room.room_id].stand(my_room_id, my_user_name):
        room.player_num -= 1
        room.viewer_num += 1
        room.player_list.remove(pusrs[0])
        room.viewer_list.add(pusrs[0])
        room.save()
        resp['succeed'] = True
        resp['message'] = " "
        return HttpResponse(json.dumps(resp))
    else:
        resp['succeed'] = False
        resp['message'] = "desk.stand() return false."
        return HttpResponse(json.dumps(resp))

def request_room_list(request):
    my_game_kind = int(request.GET.get("game_kind"))
    my_user_name = request.GET.get("user_name")

    resp = {}
    r = Room.objects.filter(game_kind=my_game_kind)
    if not r:
        resp['rooms'] = []
        return HttpResponse(json.dumps(resp))

    rooms = []
    for r in Room.objects.filter(game_kind=my_game_kind, private=False):
        room = {'room_id': r.room_id, 'game_kind': r.game_kind, 'room_name': r.room_name,
                'player_num': r.player_num, 'viewer_num': r.viewer_num, 'max_num': r.max_num, 'status': r.status}
        rooms.append(room)
    resp['rooms'] = rooms
    for r in Room.objects.filter(game_kind=my_game_kind):
        print(r)

    return HttpResponse(json.dumps(resp))


def request_game_info(request):
    my_room_id=int(request.GET.get("room_id"))
    my_user_name=request.GET.get("user_name")
    # search room
    resp = {}
    r = Room.objects.get(room_id=my_room_id)
    if not r: # room does not exist
        resp['message'] = "game does not exist"
        return HttpResponse(json.dumps(resp))
    resp["room_name"] = r.room_name
    resp["view_cnt"] = r.viewer_num
    print(desks)
    desk = desks[r.room_id]
    your_id=desk.get_user_seat_id(my_user_name)
    pod = {}
    pod["playing"]=desk.pod_info.playing
    pod["your_id"]=your_id
    pod["curr_id"]=desk.pod_info.curr_id
    pod["bookmarker_id"]=desk.pod_info.dealer+1
    pod["term"]=desk.pod_info.term
    pod["pod_chip_cnt"]=desk.pod_info.pod_chip_cnt
    pod["pokes"]=desk.pod_info.pokes
    resp["pod_info"]=pod
    resp["user_infos"]=desk.get_player_info(my_user_name)
    last_act={}
    last_act["user_id"]=desk.last_info.user_id
    last_act["action_type"]=desk.last_info.action_type
    last_act["raise_num"]=desk.last_info.raise_num
    resp["last_action"]=last_act
    return HttpResponse(json.dumps(resp))


def start_game(request):
    rid=int(request.GET.get("room_id"))
    r = models.Room.objects.filter(room_id=rid)
    print(desks)
    if r[0]:
        if r[0].room_id == rid:
            if r[0].player_num<2:
                resp={}
                resp['succeed'] = False
                resp['message'] = "num of players less than 2"
                return HttpResponse(json.dumps(resp))
            print("preparing new game")
            desks[rid].start_game(rid)
            resp={}
            resp['succeed'] = True
            resp['message'] = "游戏开始"
            return HttpResponse(json.dumps(resp))
        else:
            resp={}
            resp['succeed'] = False
            resp['message'] = "不存在该房间"
            return HttpResponse(json.dumps(resp))
    else:
        resp={}
        resp['succeed'] = False
        resp['message'] = "不存在该房间"
        return HttpResponse(json.dumps(resp))

# known bugs: 1, check if action_player and cur_player is the same player.
#                for example: when it is playerA's turn, playerB cannot fold or raise.
#             2, raise should decrease stack_cnt.
def action(request):
    my_username = request.GET.get("user_name")
    action_type = int(request.GET.get("action_type"))
    raise_num = int(request.GET.get("raise_num"))
    my_room_id = int(request.GET.get("room_id"))
    
    resp = {}
    rs = Room.objects.filter(room_id=my_room_id)
    if not rs:
        resp['succeed'] = False
        resp['message'] = "Room "+str(my_room_id)+" does not exists."
        return HttpResponse(json.dumps(resp))
    r = rs[0]
    pusrs = r.player_list.filter(username=my_username)
    if not pusrs:
        resp['succeed'] = False
        resp['message'] = "User "+my_username+" is not sitting in Room "+str(my_room_id)+"."
        return HttpResponse(json.dumps(resp))
    if (action_type < 0) or (action_type > 2):
        resp['succeed'] = False
        resp['message'] = "Invalid action type."
        return HttpResponse(json.dumps(resp))
    d = desks[r.room_id]    

    seat_id = d.get_user_seat_id(my_username)
    user_id = seat_id - 1
    # Fold
    if action_type == 0:
        d.user_info[user_id].folded = True
        d.user_info[user_id].hand_pokers = [0, 0]
    # Check
    # Call
    elif action_type == 1:
        if d.user_info[user_id].stack_cnt + d.user_info[user_id].chip_cnt < raise_num:
            resp['succeed'] = False
            resp['message'] = "Insufficient chip."
            return HttpResponse(json.dumps(resp))
        else:
            d.user_info[user_id].flag = True
            # d.pod_info.pod_chip_cnt += (raise_num-d.user_info[user_id].chip_cnt)
            d.user_info[user_id].stack_cnt -= (raise_num - d.user_info[user_id].chip_cnt)
            d.user_info[user_id].chip_cnt = raise_num

    # Raise
    elif action_type == 2:
        
        if d.user_info[user_id].stack_cnt + d.user_info[user_id].chip_cnt < raise_num:
            resp['succeed'] = False
            resp['message'] = "Insufficient chip."
            return HttpResponse(json.dumps(resp))
        else:
            d.user_info[user_id].flag = True
            # d.pod_info.pod_chip_cnt += (raise_num-d.user_info[user_id].chip_cnt)
            d.user_info[user_id].stack_cnt -= (raise_num - d.user_info[user_id].chip_cnt)
            d.user_info[user_id].chip_cnt = raise_num

    d.action(seat_id, action_type, raise_num)

    pnum = 0
    for u in d.user_info:
        if u.folded == False:
            pnum += 1
    if pnum == 1:
        # TODO: win
        d.pod_info.term = 2
        d.round_end()
        d.action(-1, 5, 0)
        resp['succeed'] = True
        resp['message'] = ""
        return HttpResponse(json.dumps(resp))

    chip = -1
    flag = True
    for u in d.user_info:
        if u.flag == False and u.folded == False:
            break
        if u.folded == False:
            if chip == -1:
                chip = u.chip_cnt
            if chip != u.chip_cnt:
                flag = False
                break
    if flag == True:
        d.round_end()
        d.action(-1, 4, 0)
        # TODO: A new term
    # Move onto the next player 
    cur_index = d.pod_info.curr_id-1
    cur_index = (cur_index+1)%8
    while d.user_info[cur_index].folded == True:
        cur_index = (cur_index+1)%8
    d.pod_info.curr_id=cur_index+1

    resp['succeed'] = True
    resp['message'] = ""
    return HttpResponse(json.dumps(resp))
