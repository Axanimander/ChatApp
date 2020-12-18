from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
import datetime
import json
# Create your views here.
from . import models
from . import forms

def index(request, tag=None):
    room_name = None
    username = None
    
    if(request.method == "GET"):
        
        room_form = forms.roomForm(request.GET)
        message_form = forms.messageForm(request.GET)
        search_form = forms.top_search_form(request.GET)
        if room_form.is_valid() and room_form.filled() :
            room_form.save(request)
        if(search_form.is_valid()):
            print(f'The type is {search_form.get_type()}')
            if(search_form.get_type() == "1"):
              
                tag = search_form.get_results()
            if(search_form.get_type() == "2"):
                room_name = search_form.get_results()
            if(search_form.get_type() == "3"):
                username = search_form.get_results()
    else:
        search_form = forms.top_search_form(request.POST)
        message_form = forms.messageForm()
        room_form = forms.roomForm()
    room_list = buildroomlist(tag, room_name, username)["rooms"]

    context = {
        "title":"RoomList",
        "roomform":room_form,
        "messageform":message_form,
        "searchform":search_form,
        "roomlist":room_list
    }
    return render(request, "index.html", context=context)

def buildroomlist(tag=None, room_name = None, username = None):
    room_objects = models.roomModel.objects.all().order_by('-created')
    room_list = {}
    room_list["rooms"] = []
    if(tag):
        room_objects = models.roomModel.objects.filter(message__content__contains=tag)
    elif(room_name):
        room_objects = models.roomModel.objects.filter(roomName__contains = room_name)
    elif(username):
        room_objects = models.roomModel.objects.filter(creator__username__contains = username)
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
    following = models.Follower.objects.filter(following = user)
    print(following)
    room_messages = None
    num_messages = None
    num_followers = followers = models.Follower.objects.filter(following = user)
    followed = models.Follower.objects.filter(follower = user)
    num_followed = len(followed)
    if(request.user.id == user_id):
        room_messages = models.ChatLogMessage.objects.filter(room__creator = user_id)
        followers = models.Follower.objects.filter(following = user)
        print(room_messages)
        num_messages = len(room_messages)
        num_followers = len(followers)
    context = {
        "user" : user,
        "rooms" : rooms,
        "room_messages": room_messages,
        "num_messages": num_messages,
        "num_followers" : num_followers,
        "followed" : followed,
        "num_followed" : num_followed,
        "following" : following,
    }

    return render(request, "profile.html", context=context)
def delete_room(request, room_id):
    room_instance = models.roomModel.objects.get(pk=room_id)
    room_instance.delete()
    return redirect('/')


def follow(request, user_id):
    followee = models.User.objects.get(pk=user_id)
    follower = models.User.objects.get(pk = request.user.id)
    try:
        follow = models.Follower.objects.get(follower=follower, following=followee)
    except models.Follower.DoesNotExist:
        follow = None
    if follow != None:
        follow.delete()
    else:
        follow = models.Follower()
        follow.follower = follower
        follow.following = followee
        follow.save()
    return redirect('/profile/' + str(user_id))
