from django.shortcuts import render, redirect
from .models import BlogPostForm, UserExtra, Blog, Diary
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import markdown
from web.webapp.register import send_code_to_email, register_code
from web.control_server.server import prt_scr,screen_off,mouse_click
from django.core.paginator import Paginator
import win32api
# Create your views here.
# Outside

#TODO: compress the image
def server_prt_scr(request):

    if 'login_user' not in request.session:
        return redirect('login')
    return render(request, template_name='server.html')

def server_connected(request):
    # if request.method == 'POST':
    #     x,y,click = request.POST['x'],request.POST['y'],request.POST['click']
    # ID = request.GET.get('id', default='110')
    prt_scr()
    return HttpResponse(open('static\\screenshot\\screenshot.png','rb').read(),content_type='application/x-bmp')

def server_src_off(request):
    screen_off()
    return HttpResponse('success')

def server_click(request, x, y):
    mouse_click(x,y)
    print(win32api.GetCursorPos())
    print(x,y)
    return HttpResponse('success')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password!= password2:
            return HttpResponse('Different password.')
        userexist = User.objects.filter(username = username).exists()
        if userexist:
            return  HttpResponse('Username exist.')

        request.session['register_username'] = username
        request.session['register_passwd'] = password
        request.session['register_email'] = email
        code = send_code_to_email(email)
        register_code.add(username, code)
        if code == -1:
            return HttpResponse('Error email, check your '
                                'information again.')
        return redirect('register_verify')
    return render(request, template_name='register.html')

def register_verify(request):
    if request.method == 'POST':
        code = request.POST['verify']
        if 'register_username' in request.session:
            username = request.session['register_username']
            password = request.session['register_passwd']
            email = request.session['register_email']
            check_result = register_code.check(username, code)
            if check_result == -1:
                return HttpResponse('Code expired')
            if check_result == 0:
                return HttpResponse('Wrong code')
            if check_result == 1:
                user = User.objects.create_user(username, email, password)
                user.save()
                request.session['login_user'] = username
                return redirect('home')
        else:
            return HttpResponse('Session do not contain username')
    if 'register_username' not in request.session:
        return redirect('login')
    return render(request, template_name='register_verify.html')

def edit_user(request):
    if request.method == 'POST':
        username = request.session['login_user']
        user = User.objects.get(username = username)
        motto,pic = request.POST['motto'], request.FILES['pic']
        user_extra = UserExtra.objects.filter(user = user).exists()
        if user_extra:
            user_info = UserExtra.objects.get(user = user)
            user_info.motto = motto
            user_info.pic = pic
        else:
            user_info = UserExtra(user = user, motto = motto, pic = pic)
        user_info.save()
        return redirect('home')
    return render(request, template_name='edit_user.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['login_user'] = username
            return redirect('home')
        else:
            return HttpResponse('Login failed: User not exist or wrong password.')
    return render(request, template_name='login.html')

def log_out(request):
    if 'login_user' in request.session:
        request.session.flush()
    return redirect('login')


# Iniside
def home(request):
    if 'login_user' in request.session:
        return render(request, template_name='home.html', context=to_render(request))
    else:
        return redirect('login')

def app(request):
    if 'login_user' not in request.session:
        return redirect('login')
    return render(request, template_name='app.html', context=to_render(request))

#Show the list of blog
def blog_list(request):
    if 'login_user' not in request.session:
        return redirect('login')

    articles = Blog.objects.all()
    context = { 'articles': articles }
    return render(request, template_name='blog_list.html', context = {**to_render(request), **context})

#Show the list of diary
def diary_list(request):
    if 'login_user' not in request.session:
        return redirect('login')
    return render(request, template_name='dairy_list.html', context=to_render(request))

def progress(request):
    return render(request, template_name='progress.html', context=to_render(request))

def view_blog(request, article_id):
    if 'login_user' not in request.session:
        return redirect('login')
    article = Blog.objects.get(id = article_id)
    return render(request, template_name='view_blog.html', context = {**to_render(request), **{'article':article}})

def edit_blog(request):

    if 'login_user' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        article_post_form = BlogPostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            current_time = timezone.localtime()
            new_article.time = current_time
            new_article.save()
            return redirect('blog')
        else:
            return HttpResponse("标题与内容不能为空")
    else:
        return render(request, template_name='edit_blog.html', context=to_render(request))

def del_blog(request):
    pass
#
# def post(request):
#     pass


def to_render(request):
    if 'login_user' in request.session:
        user = User.objects.get(username = request.session['login_user'])
        user_pic = UserExtra.objects.get(user = user).pic
        user_motto = UserExtra.objects.get(user = user).motto
    return {'user_pic': user_pic, 'user_motto': user_motto}

