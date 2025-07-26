from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment, Like, FriendRequest  # Add this import
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm  

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': user_profile})

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(author=request.user, content=content)
        return redirect('feed')
    return render(request, 'create_post.html')

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(post=post, author=request.user, text=text)
    return redirect('feed')

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    Like.objects.get_or_create(post=post, user=request.user)
    return redirect('feed')

@login_required
def send_request(request, user_id):
    to_user = User.objects.get(id=user_id)
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('user_list')

@login_required
def accept_request(request, request_id):
    req = FriendRequest.objects.get(id=request_id)
    req.accepted = True
    req.save()
    return redirect('friends')

    # Add to core/views.py
def home(request):
    return redirect('login')  # Simple redirect to login page

# In core/views.py
def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return redirect('login')

# Add these URL names to your views
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Post.objects.create(author=request.user, content=content)
        return redirect('feed')
    return redirect('feed')  # Redirect back to feed if accessed via GET

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Like.objects.get_or_create(post=post, user=request.user)
    return redirect('feed')

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(post=post, author=request.user, text=text)
    return redirect('feed')


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})