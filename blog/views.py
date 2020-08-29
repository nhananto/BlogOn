from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

#Home


def home(request):
    # writter = Post.objects.filter(author_id=request.user.id)
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})
#About


def about(request):
    return render(request, 'blog/about.html')

#Contact


def contact(request):
    return render(request, 'blog/contact.html')


#Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')


#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


#Signup
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!!! You have become an author')
            user = form.save()

    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})


#Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged In Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')

# Add Post


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc, author_id=request.user.id)
                messages.success(request, 'Blog Posted...')
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# Update Post


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                messages.success(request, 'Updated successfully!!')
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
#Profile


def profile(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author_id=request.user.id)
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/profile.html', {'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return render(request, '404.html')
