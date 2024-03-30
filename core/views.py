from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room,Topic
from django. db.models import Q
from .forms import RoomForm
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
def loginpage(request):
    page = 'login'
    if request. user.is_authenticated:
        return redirect ('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect( 'home')
        else:
            messages.error(request, 'Wrong credentials')

    
    context = {'page':page}
    return render(request, 'core/reg_login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    page = 'register'
    context = {'page':page}
    return render(request, 'core/reg_login.html', context)
    
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
        
    rooms = Room.objects.filter (
    Q(topic__name__icontains=q) |
    Q(description__icontains=q) |
    Q(name__icontains=q) 
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count }
    return  render(request,'core/home.html',context  )


def room(request, pk):
    room = Room
    context = {'room': room}

    return  render(request,'core/rooms.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    
    return render (request, 'core/room_form.html',context)

@login_required(login_url='login')
def updatedRoom(request,pk):    
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You cant update ')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render (request, 'core/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You cant delete')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'core/delete.html',{'object':room})