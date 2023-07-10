from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_login(req):
    if req.method == "POST":
        form = LoginForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            user =  authenticate(
                req,username=data['username'],password=data['password'])
            if user is not None:
                login(req,user)
                return HttpResponse("user authenticated and logged in")
            else:
                return HttpResponse('Invalid credentials')
            
    else:
        form = LoginForm()
    return render(req, 'users/login.html',{'form':form})

@login_required
def index(req):
    return render(req,'users/index.html')

def register(req):
    if req.method == 'POST':
       user_form = UserRegistrationForm(req.POST)
       if user_form.is_valid():
           new_user = user_form.save(commit=False)
           new_user.set_password(user_form.cleaned_data['password'])
           new_user.save()
           return render(req,'users/register_done.html')
    else:
        user_form = UserRegistrationForm()
        return render(req,'users/register.html',{'user_form':user_form})    