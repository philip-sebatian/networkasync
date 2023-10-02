
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts/<int:pg>",views.allpost,name='allposts'),
    path('like/<int:id>',views.like,name='like'),
    path('unlike/<int:id>',views.unlike,name='unlike'),
    path('update/<int:id>',views.update),
    path('pc/<int:id>',views.post_content),
    path('follow/<int:id>',views.follow),
    path('unfollow/<int:id>',views.unfollow),
    path('profile/<int:id>/<int:pg>',views.profile,name='profile'),
    path('following/<int:pg>',views.following,name='following'),
    path('create',views.create,name='create')
    
]
