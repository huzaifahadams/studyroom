from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,Messages
from django. db.models import Q 
from .forms import RoomForm
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth. forms import UserCreationForm
def loginpage(request):
    page = 'login'
    if request. user.is_authenticated:
        return redirect ('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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

def registerPage(request):
    form =UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'an error occured during regesteraton')
            
    page = 'register'
    context = {'page':page, 'form':form}
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
    room_msgz = Messages.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count,'room_msgz':room_msgz }
    return  render(request,'core/home.html',context  )


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Messages.objects.create(
            user= request.user,
            room=room,
            body=request.POST.get('body'),
            
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
        
    context = {'room': room,'room_messages':room_messages, 'participants':participants}
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


@login_required(login_url='login')
def deleteMessage(request, pk):
    msg = Messages.objects.get(id=pk)
    if request.user != msg.user:
        return HttpResponse('You cant delete')
    if request.method == 'POST':
        msg.delete()
        return redirect(' ')
    return render(request, 'core/delete.html',{'object':msg})