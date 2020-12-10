from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
import datetime
import json
# Create your views here.
from . import models
from . import forms

def index(request, tag=None):
    if(request.method == "POST"):
        room_form = forms.roomForm(request.POST)
        message_form = forms.messageForm(request.POST)
        if room_form.is_valid():
            room_form.save(request)

    else:
        message_form = forms.messageForm()
        room_form = forms.roomForm()
    room_list = buildroomlist(tag)["rooms"]

    context = {
        "title":"RoomList",
        "roomform":room_form,
        "messageform":message_form,
        "roomlist":room_list
    }
    return render(request, "index.html", context=context)

def buildroomlist(tag=None):
    room_objects = models.roomModel.objects.all().order_by('-created')
    room_list = {}
    room_list["rooms"] = []
    if(tag):
        room_objects = models.roomModel.objects.filter(message__content__contains=tag)
    for room in room_objects:
        message_objects = models.message.objects.filter(room=room)
        temp_room = {}
        temp_room["id"] = room.id
        temp_room["roomName"] = room.roomName
        temp_room["timeout"] = room.created
        temp_room["creator"] = room.creator
        temp_room["messages"] = message_objects
        room_list["rooms"] += [temp_room]
    return room_list

def addmessage(request, room_id):
    print(request.method)
    if request.method == "POST":
        print("adding message")
        form = forms.messageForm(request.POST)
        if(form.is_valid()):
            form.save(request, room_id)
            return redirect("/")
    else:
        form = forms.messageForm()
    room_list = buildroomlist()["rooms"]
    context = {
        "title":"Message",
        "room_list":room_list,
        "form":form,
    }
    return render(request, "index.html", context=context)

def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if(user is not None):
        login(request, user)
        return redirect('/')
    else:
        return redirect('/')
        
def myregister(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if(form_instance.is_valid()):
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form": form_instance,        
    }
    return render(request, "registration/register.html", context=context)

def room(request, room_id):
    room_object = models.roomModel.objects.get(id=room_id)
    message_log = models.ChatLogMessage.objects.filter(room=room_object)
    message_log_json = json.loads(serializers.serialize('json', message_log))
    users_log = models.chatUser.objects.filter(room=room_object)
    users_log_json = json.loads(serializers.serialize('json', users_log))
    return render(request, 'room.html', {
        'room_id': room_id,
        'user_id': request.user.username,
        'user_link' : request.user.id,
        'roomname':room_object.roomName,
        'message_log': message_log_json,
        'users_log': users_log_json,
    })

def logout_view(request):
    logout(request)
    return redirect("/login/")


def profile_view(request, user_id):
    user = models.User.objects.get(pk=user_id)
    rooms = models.roomModel.objects.filter(creator=user_id)
    
    context = {
        "user" : user,
        "rooms" : rooms,
    }

    return render(request, "profile.html", context=context)