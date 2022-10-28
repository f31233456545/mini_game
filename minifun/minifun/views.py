from django.http import HttpResponse
from django.shortcuts import render
import json
from room.models import Room
from room.admin import id_counter

# this is a test function.
def hello(request):
    return HttpResponse("Hello world ! ")


# this is a test function.
def template(request):
    views_dict = {"name":"菜鸟教程"}
    return render(request, "views_dict.html", {"views_dict": views_dict})

# login function
def login(request):
    # get param 'username'
    username = request.GET.get("username")
    # get param 'password'
    password = request.GET.get("password")
    # create a python dictionary
    resp = {}
    resp['message']="success"
    resp['succeed']=True
    # convert dict to json
    return HttpResponse(json.dumps(resp))

# register function
def register(request):
    # get param 'username'
    username = request.GET.get("username")
    # get param 'password'
    password = request.GET.get("password")
    # create a python dictionary
    resp = {}
    resp['message']="success"
    resp['succeed']=True
    # convert dict to json
    return HttpResponse(json.dumps(resp))

# create a room function
def create_room(request):
    # Note: After the creator creates the room, he needs manually send a join_room request to join the room.
    # TODO: should we auto join_room after create_room?
    global id_counter
    my_private = request.GET.get("private")     # default: 0, that is a public room
    my_room_name = request.GET.get("room_name")
    my_game_kind = request.GET.get("game_kind")     # default: Texas Hold'em poker
    my_creator_name = request.GET.get("creator_name")
    my_max_num_int = 13     # default: 8 players and 5 viewers at most.
    # TODO: self-defined capacity of the room?  
    # my_max_num = request.GET.get("max_num")
    # if not my_max_num:
    #     my_max_num = '13'
    # my_max_num_int = int(my_game_kind)

    resp={}
    if ((not my_room_name) or (not my_creator_name)) :
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
    id_counter = id_counter+1
    r = Room(room_id=id_counter, private=my_private_bl, 
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

    resp={}
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
    r = Room.objects.filter(room_id=my_room_id_int)[0]
    print(r)
    if not r:
        resp['succeed'] = False
        resp['message'] = "Room "+my_room_id+" does not exist."
        return HttpResponse(json.dumps(resp))
    if r.player_num+r.viewer_num>r.max_num:
        resp['succeed'] = False
        resp['message'] = "Room "+my_room_id+" is filled to capacity."
        return HttpResponse(json.dumps(resp))
    # TODO: check if the user is already in the room
    # TODO: a conception: blacklist?
    #tmp_usr = r.viewer_list.get(username=my_username)
    #if tmp_usr:
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

# def request_room_list(request)
