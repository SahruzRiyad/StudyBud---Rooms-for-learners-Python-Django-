from django.shortcuts import render
from .models import Room
from .forms import RoomForm


# Create your views here.


def home(request):
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request, 'home.html' , context)

def room(request , pk):
    room = Room.objects.get(id=pk)
    context = {'room' : room}
    return render(request, 'room.html', context)

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        print(request.POST)
    context = {'form': form}
    return render(request , 'base/room_form.html' , context)