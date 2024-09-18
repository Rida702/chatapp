from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Room, Chat
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    return render(request, 'registration/home.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('select_user')
    return render(request, "chat/index.html")

@login_required
def room(request, room_name):
    user_1 = request.session.get('user_1')
    user_2 = request.session.get('user_2')
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "user_1": user_1,
        "user_2": user_2,
    })

@login_required
def select_user(request):
    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('user_ids')
        
        for selected_user_id in selected_user_ids:
            selected_user = User.objects.get(id=selected_user_id)

            user_ids = sorted([request.user.id, selected_user.id])
            room_name = f"{user_ids[0]}_{user_ids[1]}_chat"

            request.session['user_1'] = request.user.first_name
            request.session['user_2'] = selected_user.first_name
        

            room, created = Room.objects.get_or_create(name=room_name)

            Chat.objects.create(room=room, user_1=request.user, user_2=selected_user, message=None)

            return redirect('room', room_name=room_name)

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {'users': users})