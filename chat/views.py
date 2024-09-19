from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Room, Chat
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name": room_name,
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from chat.models import Room

@login_required
def select_user(request):
    if request.method == 'POST':
        chat_type = request.POST.get('chat_type')

        room_name = None

        if chat_type == '1to1_chat':
            selected_user_id = request.POST.get('user_ids')  
            if selected_user_id:
                selected_user = User.objects.get(id=selected_user_id)
                user_ids = sorted([request.user.id, selected_user.id])
                room_name = f"{user_ids[0]}_{user_ids[1]}_chat"
            else:
                messages.error(request, "Please select a user to start a 1-on-1 chat.")
                return redirect('select_user')

        elif chat_type == 'group_chat':
            group_name = request.POST.get('group_name').strip() 
            if group_name:
                room_name = group_name 
            else:
                messages.error(request, "Please enter a group name.")
                return redirect('select_user')


        if room_name:
            room, created = Room.objects.get_or_create(name=room_name)

            return redirect('room', room_name=room.name)

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {'users': users})

"""
@login_required
def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name').strip()  

        if group_name:
            room, created = Room.objects.get_or_create(name=group_name)

            return redirect('room', room_name=room.name)  

    return render(request, 'chat/index.html')
"""