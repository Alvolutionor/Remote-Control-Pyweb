from django.contrib import admin
from web.views import home, blog_list, app, diary_list, progress, view_blog, \
    edit_blog, login, register, register_verify, log_out, edit_user, \
    server_prt_scr, server_src_off, server_connected,server_click

from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('', home,name = 'home'),
    # path('blog/', blog_list, name = 'blog'),
    path('server/', server_prt_scr, name = 'server'),
    path('server/off', server_src_off),
    path('server/server_connected',server_connected),
    path('login/', login, name = 'login'),
    path('log_out/', log_out, name='log_out'),
    path('register/', register, name = 'register'),
    path('edit_user/', edit_user, name='edit_user'),
    path('app/', app, name = 'app'),
    path('diary/', diary_list, name = 'diary'),
    path('blog/', blog_list, name = 'blog'),
    path('edit_blog/', edit_blog, name='edit_blog'),
    path('progress/', progress, name = 'progress'),
    path('register_verify/', register_verify, name = 'register_verify'),
    path('view_blog/<int:article_id>', view_blog, name='view_blog'),

    path('server/server_click/<int:x>/<int:y>', server_click),
]






