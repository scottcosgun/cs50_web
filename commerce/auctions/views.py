from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment


def index(request):
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "categories": Category.objects.all()
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'auctions/create_listing.html', {
            "categories": categories
        })
    
    if request.method == 'POST':
        # Get info from form
        name = request.POST['name']
        description = request.POST['description']
        img_url = request.POST['img_url']
        price = request.POST['bid']
        category = request.POST['category']
        curr_user = request.user

        # Create a bid
        bid = Bid(bid=float(price), user=curr_user)
        bid.save()

        # Select category
        try:
            selected_cat = Category.objects.get(category_name=category)
        except:
            selected_cat = None

        # Create listing object and save into database
        l = Listing(
            name=name,
            owner=curr_user,
            description=description,
            img_url=img_url,
            price=bid,
            category=selected_cat
            )
        l.save()
        # Redirect to index page
        return HttpResponseRedirect(reverse(index))

def category_filter(request):
    if request.method == "POST":
        selected_cat = request.POST['category']
        try:
            category = Category.objects.get(category_name=selected_cat)
            active_listings = Listing.objects.filter(active=True, category=category)
        except:
            category = Category.objects.all()
            active_listings = Listing.objects.filter(active=True)
        return render(request, "auctions/index.html", {
            "active_listings": active_listings,
            "categories": Category.objects.all()
        })
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    in_watchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    curr_is_owner = (request.user.username == listing.owner.username)
    return render(request, "auctions/listing.html", {
        "listing":listing,
        "in_watchlist": in_watchlist,
        "comments": comments,
        "curr_is_owner":curr_is_owner
    })

def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    curr_user = request.user
    listing.watchlist.remove(curr_user)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    curr_user = request.user
    listing.watchlist.add(curr_user)
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def watchlist(request):
    curr_user = request.user
    watchlist_listings = curr_user.listing_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": watchlist_listings
    })

def add_comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    curr_user = request.user
    user_comment = request.POST['new_comment']

    new_comment = Comment(
        author=curr_user,
        listing=listing,
        user_comment=user_comment
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

def add_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid_amt = float(request.POST['new_bid'])
    if bid_amt > listing.price.bid:
        new_bid = Bid(user=request.user, bid=bid_amt)
        new_bid.save()
        listing.price = new_bid
        listing.save()
        message, update = "Bid successful", True
    else:
        message, update = "Bid failed", False

    return render(request, "auctions/listing.html", {
        "listing":listing,
        "message":message,
        "update":update,
        "comments":Comment.objects.filter(listing=listing),
        "in_watchlist":request.user in listing.watchlist.all()
    })

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    curr_is_owner = (request.user.username == listing.owner.username)
    return render(request, "auctions/listing.html", {
        "listing":listing,
        "message":"Auction successfully closed",
        "update":True,
        "curr_is_owner": curr_is_owner,
        "comments":Comment.objects.filter(listing=listing),
        "in_watchlist":request.user in listing.watchlist.all()
    })