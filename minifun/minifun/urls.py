"""minifun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('template/', views.template),
    path('login/', views.login),
    path('register/', views.register),
    path('create_room/', views.create_room),
    path('join_room/', views.join_room),
    path('sit/', views.sit),
    path('stand/', views.stand),
    path('exit_room/', views.exit_room),
    path('request_room_list/', views.request_room_list),
    path('request_game_info/', views.request_game_info),
    path('start_game/', views.start_game),
    path('action/', views.action),
    path('testDetermineWinner/', views.testDetermineWinner),
]
