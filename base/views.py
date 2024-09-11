from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, CustomUserCreationForm
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist.")


    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = CustomUserCreationForm()
    context = {'form' : form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')

        else:
            messages.error(request, str(form.errors))

    return render(request, 'base/register.html', context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user' : user, 'rooms' : rooms,
               'room_messages' : room_messages, 'topics' : topics}

    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect ('user-profile',pk=user.id)
        else:
            messages.error(request, "Username/Email is not valid!!")

    context = {'form' : form}

    return render(request, 'base/update-user.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))


    context = {'rooms' : rooms, 'topics' : topics, 
               'room_count' : room_count, 'room_messages' : room_messages}
    return render(request, 'home.html' , context)

def room(request , pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context = {'room' : room, 'room_messages' : room_messages, 'participants' : participants}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        try:
            Room.objects.create(
                host = request.user,
                topic = topic,
                name = request.POST.get('name'),
                description = request.POST.get('description')

            )
            return redirect('home')
        
        except Exception as e:
            messages.error(request, f'Error creating room: {e}')
        
    context = {'form': form, 'topics' : topics}
    return render(request , 'base/create_room.html' , context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to update others room.')
    
    if request.method == 'POST':

        room_name = request.POST.get('room_name')
        topic_name = request.POST.get('topic')
        description = request.POST.get('room_about')

        topic, created = Topic.objects.get_or_create(name=topic_name)

        try:
            room.name = room_name
            room.description = description
            room.topic = topic

            print(description)
            room.save()
            return redirect('room', pk=room.id)
        
        except Exception as e:
            messages.error(request, f'Error creating room: {e}')

    context = {'topics' : topics, 'room' : room}

    return render(request, 'base/update-room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    context = {'obj' : room}

    if request.user != room.host:
        return HttpResponse('You are not allowed to delete others room.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    context = {'obj' : message}

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete others room.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', context)