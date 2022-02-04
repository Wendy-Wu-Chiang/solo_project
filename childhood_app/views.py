from django import views
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
# import os
# from moviepy.editor import VideoFileClip
# os.environ["IMAGEIO_FFMPEG_EXE"] = "/Users/xiaoyuewu/Desktop/solo_project/py3Env/lib/python3.9/site-packages/imageio/plugins/ffmpeg.py"




def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hashed_pw
        )
        request.session['logged_user'] = new_user.id
        return redirect('/dashboard')

    return redirect('/')


def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/dashboard')
        messages.error(request, "Email or password are incorrect.")

    return redirect("/")


def dashboard(request):

    context = {
        'all_contents': Experience.objects.all(),
        'logged_user': User.objects.get(id=request.session['logged_user']),
    }
    return render(request, 'dashboard.html', context)


def create_content(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')

    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'content': Experience.objects.all(),
    }

    return render(request, 'create_content.html', context)


def create(request):
    if request.method == 'POST':
        errors = Experience.objects.content_validator(request.POST, request.FILES)
        user = User.objects.get(id=request.session['logged_user'])
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/contents/new')

        this_user_content = Experience.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            videofile = request.FILES['videofile'],
            user_content = user
        )
       
        return redirect('/dashboard')
    return redirect('/dashboard')


def content(request, content_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    user = User.objects.get(id=request.session['logged_user'])
    content = Experience.objects.get(id=content_id)
    user.viewed_contents.add(content)
    # views = Experience.objects.get(id=content_id)
    # content.views.add(views)
    context = {
        'logged_user': user,
        'content': content,
    }
    return render(request, 'view_content.html', context)


def edit(request, content_id):
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'content': Experience.objects.get(id=content_id)
    }
    return render(request, 'edit.html', context)


def update(request,content_id):
    if request.method == 'POST':
        errors = Experience.objects.content_validator(request.POST, request.FILES)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/contents/edit/{content_id}')
        else:
            to_update = Experience.objects.get(id=content_id)
            to_update.title = request.POST['title']
            to_update.content = request.POST['content']
            if "videofile" in request.FILES:
                to_update.videofile = request.FILES['videofile']
            to_update.save()
        return redirect('/dashboard')
    return redirect('/')

# def total_views(request, content_id):
    


       
def likes(request, content_id):
    user = User.objects.get(id=request.session['logged_user'])
    content = Experience.objects.get(id=content_id)
    user.liked_contents.add(content)
    

    return redirect(f'/contents/{content_id}')

def unlike(request, content_id):
    user = User.objects.get(id=request.session['logged_user'])
    content = Experience.objects.get(id=content_id)
    user.liked_contents.remove(content)

    return redirect(f'/contents/{content_id}')    

def post_comment(request, content_id):
    poster = User.objects.get(id=request.session['logged_user'])
    content = Experience.objects.get(id=content_id) 
    print(content.content_comments)
    new_common = Comment.objects.create(comment=request.POST['comment'], poster=poster, content=content)
    content.content_comments.add(new_common)
    print(content.content_comments)
    return redirect(f'/contents/{content_id}')
    
def delete_comment(request,content_id, comment_id):
# def delete_comment(request, comment_id):
    # content = Experience.objects.get(id=content_id) 
    # destroyed = Comment.objects.get(id=comment_id)
    # destroyed = Comment.objects.get(id=id)
    destroyed = Comment.objects.get(id=comment_id)
    destroyed.delete()
    return redirect(f'/contents/{content_id}')

def cancle(request):
    return redirect('/dashboard')


def delete(request, content_id):
    to_delete = Experience.objects.get(id=content_id)
    to_delete.delete()
    return redirect('/dashboard')


def logout(request):
    request.session.flush()
    return redirect('/')
