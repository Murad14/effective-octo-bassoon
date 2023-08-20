from django.shortcuts import render,redirect
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.shortcuts import get_object_or_404


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

def feed(req):
    if req.method == 'POST':
        comment_form = CommentForm(data=req.POST)
        new_comment = comment_form.save(commit=False)
        post_id = req.POST.get('post_id')
        post = get_object_or_404(Post,id=post_id)
        new_comment.post = post
        new_comment.save()
    else:
        comment_form = CommentForm()
    
    posts = Post.objects.all()
    logged_user = req.user
    return render(req, 'posts/feed.html', {'posts': posts, 'logged_user':logged_user, 'comment_form':comment_form})

def like_post(req):
    post_id = req.POST.get('post_id')
    post = get_object_or_404(Post,id=post_id)
    if post.liked_by.filter(id=req.user.id).exists():
        post.liked_by.remove(req.user)
    else:
        post.liked_by.add(req.user)
    return redirect('feed')

@login_required
def add_comment(req):
    if req.method == 'POST':
        post_id = req.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        body = req.POST.get('body')
        new_comment = Comment(post=post, posted_by=req.user, body=body)
        new_comment.save()
    return redirect('feed')
