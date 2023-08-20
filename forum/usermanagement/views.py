from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Userinfo

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User exists
            login(request, user)
            return redirect('homepage')
        else:
            return redirect('login')
    else:
        return render(request, 'usermanagement/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

 
def register_user(request):
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            print(register_form.cleaned_data.get("username"))
            new_user = User.objects.get(username=register_form.cleaned_data.get("username"))
            print(new_user)
            insert_new_user = Userinfo(user_id=new_user)
            insert_new_user.save()
            messages.success(request, f'Successfully registered!')
            return redirect('login')
        else:
            messages.error(request, "Account already exists")
            return redirect('register')
    else:
        register_form  = UserCreationForm()
        return render(request, 'usermanagement/register.html', {'form': register_form})
