from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Room, Topic, Messages
from .forms import Room_form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist.")
        
    context = {'page':page}
    return render(request, 'login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    context = {'page':page, 'form':form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Something went wrong')
    return render(request,'login_register.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms_info = Room.objects.filter(
                Q(topic__name__icontains=q)|
                Q(name__icontains = q) |
                Q(description__icontains = q))
    
    topics = Topic.objects.all()
    room_messages = Messages.objects.filter(Q(room__topic__name__icontains =q))
    room_count = rooms_info.count()
    context = {'rooms_info':rooms_info,'topics':topics, 'room_count': room_count,'room_messages':room_messages}
    return render(request,'home.html',context)

def rooms(request,id):
    room = Room.objects.get(id = id)
    room_messages = room.messages_set.all().order_by('-created')
    participants = room.participants.all()
    participants_count = participants.count()
    if request.method == 'POST':
        message = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id = room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants,'participants_count':participants_count}
    return render(request,'room.html',context)

def userProfile(request,id):
    user = User.objects.get(id=id)
    rooms_info = user.room_set.all()
    room_messages = user.messages_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms_info':rooms_info,'room_messages':room_messages,'topics':topics}
    return render(request, 'profile.html',context)

@login_required(login_url='/login')
def create_room(request):
    form = Room_form
    context = {'form':form}
    if request.method == 'POST':
        form = Room_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'room_form.html',context)

@login_required(login_url='/login')
def update_room(request,pk):
    room = Room.objects.get(id = pk)
    form = Room_form(instance=room)
    context = {'form':form}
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        form = Room_form(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'room_form.html',context)

@login_required(login_url='/login')
def delete_room(request, pk):
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    room = Room.objects.get(id=pk)
    context = {'obj':room}
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'delete.html',context)
    
@login_required(login_url='/login')
def delete_message(request, pk):
    message = Messages.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    context = {'obj':message}
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'delete.html',context)