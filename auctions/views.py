from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bids, Category


def index(request):
    return render(request, "auctions/index.html", {
        "listing": Listing.objects.all()
    })

@login_required
def create_listing_view(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["value"]
        img_url = request.POST["image_url"]
        category = Category.objects.get(id=(request.POST["category_id"]))
        item = Listing(title=title, descripition=description,
                       start_bid=bid, image_url=img_url,
                       category=category, owner=user)
        item.save()
        return render(request, "auctions/listing.html", {
            "message":"Added with success"
        })
    categories = Category.objects.all()
    return render(request, "auctions/listing.html", {
        "categories": categories
    })

def item_view(request, item_id):
    item = Listing.objects.get(id=item_id)
    on_list = False
    if not item:
        return render("auctions/index.html", {
            "message": f"Item {item_id} does not exist.",
        })
    if request.method == "POST":
        d_item = item.delete()
        return HttpResponseRedirect(reverse("index"))
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        watchlist = user.user_watchlist.all()
        if watchlist.filter(id=item_id).exists():
            on_list = True
    return render(request, "auctions/item.html", {
        "item": item,
        "on_list": on_list
    })


@login_required
def watchlist_view(request, item_id=''):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        item = Listing.objects.get(id=item_id)
        if item in user.user_watchlist.all():
            user.user_watchlist.remove(item)
        else:
            user.user_watchlist.add(item)
        return HttpResponseRedirect(reverse("item", args=(item.id,)))
    items = user.user_watchlist.all()
    return render(request, "auctions/watchlist.html", {
                  "items": items
                  })


@login_required
def bid_view(request, item_id):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        amount = float(request.POST["amount"])
        item = Listing.objects.get(id=item_id)
        bid = item.current_bid
        if bid:
            if amount > bid.value:
                cur_bid = Bids(bidder=user, value=amount)
                cur_bid.save()
                item.current_bid = cur_bid
                item.save()
            else:
                return render(request, "auctions/item.html", {
                    "item": item,
                    "on_list": user.user_watchlist.all().filter(id=item_id).exists(),
                    "message": "The bid has to be grater than the starting bid and the current bid"
                })
        else:
            if amount > item.start_bid:
                cur_bid = Bids(bidder=user, value=amount)
                cur_bid.save()
                item.current_bid = cur_bid
                item.save()
            else:
                return render(request, "auctions/item.html", {
                    "item": item,
                    "on_list": user.user_watchlist.all().filter(id=item_id).exists(),
                    "message": "The bid has to be grater than the starting bid and the current bid"
                })
        return HttpResponseRedirect(reverse("item", args=(item.id,)))


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
