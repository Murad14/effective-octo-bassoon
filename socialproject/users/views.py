from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from posts.models import Post


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
    current_user = req.user
    posts = Post.objects.filter(user=current_user)
    return render(req,'users/index.html',{'posts':posts})

def register(req):
    if req.method == 'POST':
       user_form = UserRegistrationForm(req.POST)
       if user_form.is_valid():
           new_user = user_form.save(commit=False)
           new_user.set_password(user_form.cleaned_data['password'])
           new_user.save()
           Profile.objects.create(user=new_user)
           return render(req,'users/register_done.html')
    else:
        user_form = UserRegistrationForm()
        return render(req,'users/register.html',{'user_form':user_form})  

@login_required # type: ignore
def edit(req):
    if req.method == 'POST':
        user_form = UserEditForm(instance=req.user,data=req.POST)
        profile_form = ProfileEditForm(
            instance=req.user.profile,data=req.POST,files=req.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponse('Profile updated successfully.')
    else:
        user_form = UserEditForm(instance=req.user)
        profile_form = ProfileEditForm(
            instance=req.user.profile)
        return render(req, 'users/edit.html',{'user_form':user_form,'profile_form':profile_form})