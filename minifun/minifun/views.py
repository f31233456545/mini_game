from django.http import HttpResponse
from django.shortcuts import render
import json

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