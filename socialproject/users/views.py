from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from .forms import LoginForm
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