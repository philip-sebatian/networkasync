from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
import rest_framework
from rest_framework import generics
from rest_framework.response import Response
from .serializer import PostSerializer
from .models import User
from . models import *
import json
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.core.paginator import Paginator



def index(request):
    return HttpResponseRedirect(reverse('allposts',args=[1]))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

def allpost(request,pg):
    objects=Post.objects.all()
    p=Paginator(objects,10)
    page=p.page(pg)


    return render(request,'network/allposts.html',{
        'posts':page.object_list,'p':p
    })


def like(request,id):
    if request.method=="POST":
        x=Post.objects.get(id=id)
        
        print(x.content)
        x.liked_by.add(request.user)
        x.save()
        return JsonResponse({"status":"successfully liked"})

def unlike(request,id):
   if request.method=="POST":
        
        x=Post.objects.get(id=id)
        print(x.content)
        x.liked_by.remove(request.user)
        x.save()
        return JsonResponse({"status":"successfully unliked"})
   
def update(request,id):
    if request.method=="POST":
        print(request.body)
        data=request.body
        string=data.decode('utf-8')
        x=json.loads(string)
        post=Post.objects.get(id=id)
        post.content=x['content']
        post.save()
        return JsonResponse({"hi":"hi"})
    
def post_content(request,id):
    post=Post.objects.get(id=id)
    return JsonResponse({'content':post.content})
        
def profile(request,id,pg):
    user=User.objects.get(id=id)
    posts=Post.objects.filter(owner=user)
    p=Paginator(posts,10)
    page=p.page(pg)
    return render(request,'network/profile.html',{
        'posts':page.object_list,'user':user,'p':p
    })


def follow(request,id):
    post_owner=User.objects.get(id=id)
    post_owner.followers.add(request.user)
    post_owner.save()
    user=User.objects.get(id=request.user.id)
    user.following.add(post_owner)
    return JsonResponse({'status':'successfull'})


def unfollow(request,id):
    post_owner=User.objects.get(id=id)
    post_owner.followers.remove(request.user)
    post_owner.save()
    user=User.objects.get(id=request.user.id)
    user.following.remove(post_owner)
    return JsonResponse({'status':'successfull'})



def following(request,pg):
    posts=[]
   
    for i in request.user.following.all():
        for j in Post.objects.filter(owner=i):
            posts.append(j)
    print(posts)
    p=Paginator(posts,10)
    page=p.page(pg)

    return render(request,'network/following.html',{
        'posts':page.object_list,'p':p
    })

