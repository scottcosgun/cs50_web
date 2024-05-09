from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import User, Post, Follow, Like


def index(request):
    all_posts = Post.objects.all().order_by('id').reverse()
    p = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    user_liked_posts = list(Like.objects.filter(user=request.user).values_list('liked_post_id', flat=True))

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "all_posts": all_posts,
        'user_liked_posts':user_liked_posts
    })

def new_post(request):
    if request.method == "POST":
        text = request.POST['text']
        author = User.objects.get(pk=request.user.id)
        post = Post(text=text, user=author)
        post.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, user_id):
    # Get user
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by('id').reverse()

    # Following + followers counts
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(followed=user)

    # Logic for follow and unfollow button
    if user != request.user:
        is_following = followers.filter(user=request.user).exists()
    else:
        is_following = False

    # Implement pagination, with no more than 10 posts on a single page
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/profile.html", {
        "page_obj":page_obj,
        "posts":posts,
        "username":user.username,
        "following":following,
        "followers":followers,
        "is_following":is_following,
        "current_user":user
    })
    
def follow_unfollow(request, user_id, followed_id):
    if request.method == "POST":
        current_user = User.objects.get(pk=user_id)
        followed = User.objects.get(pk=followed_id)
        # User signed in should only be able to follow other accounts
        if current_user != followed:
            # Unfollow account
            try:
                follow_obj = Follow.objects.get(user=current_user, followed=followed)
                follow_obj.delete()
            # Follow account
            except:
                follow_obj = Follow(user=current_user, followed=followed)
                follow_obj.save()
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':followed_id}))

def following(request):
    current_user = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('id').reverse()
    user_liked_posts = list(Like.objects.filter(user=request.user).values_list('liked_post_id', flat=True))
    # Create a list of all posts written by people the current user is following
    followed_posts = [post for post in all_posts if any(person.followed == post.user for person in following)]

    # Implement pagination
    p = Paginator(followed_posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "all_posts": followed_posts,
        "user_liked_posts":user_liked_posts
    })

def edit(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        if post.user == request.user:
            if request.method == 'POST':
                data = json.loads(request.body)
                updated_text = data.get('text')

                if updated_text:
                    # Update post with new text
                    post.text = updated_text
                    post.save()

                    # Return a JSON response with the updated text
                    return JsonResponse({'updated_text': updated_text})
                else:
                    return JsonResponse({'error': 'Updated text cannot be empty'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid request method'}, status=400)
        else:
            return JsonResponse({'error': 'You are not allowed to edit this post'}, status=403)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

def get_like_count(request, post_id):
    try:
        like_count = Like.objects.filter(liked_post_id=post_id).count()
        return JsonResponse({'like_count': like_count})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def like(request, post_id):
    if request.method == "POST":
        user = request.user
        post = Post.objects.get(pk=post_id)
        like_count = Like.objects.count()
        # Unlike post
        like = Like.objects.filter(user=user, liked_post=post)
        if like:
            like.delete()
            is_liked = False
        else:
            # Create a new Like object for this user and post
            like = Like.objects.create(user=user, liked_post=post)
            like.save()
            is_liked = True
        # Update like count and return in json response
        like_count = Like.objects.filter(liked_post=post).count()
        return JsonResponse({'like_count':like_count, 'is_liked':is_liked})
    # Error if request.method is not post
    return JsonResponse({'error':'Invalid request method'}, status=400)

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
