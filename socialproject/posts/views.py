from django.shortcuts import render
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def post_create(req):
    if req.method == 'POST':
        form = PostCreateForm(data=req.POST,files=req.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = req.user
            new_item.save()
    else:
        form = PostCreateForm(data=req.GET)
        
    return render(req,'posts/create.html',{'form':form})