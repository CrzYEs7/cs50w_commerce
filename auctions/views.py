from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import AddListingForm, AddCommentForm
from .models import User, Listing, Bids, Category, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "listing": Listing.objects.all()
    })

@login_required
def create_listing_view(request):
   # if request.method == "POST":
   #     user = User.objects.get(id=request.user.id)
   #     title = request.POST["title"]
   #     description = request.POST["description"]
   #     bid = request.POST["value"]
   #     img_url = request.POST["image_url"]
   #     category = Category.objects.get(id=(request.POST["category_id"]))
   #     item = Listing(title=title, descripition=description,
   #                    start_bid=bid, image_url=img_url,
   #                    category=category, owner=user)
   #     item.save()
   #     return render(request, "auctions/listing.html", {
   #         "message":"Added with success"
   #     })

   # # Add new listing form
   # categories = Category.objects.all()
   # return render(request, "auctions/listing.html", {
   #     "categories": categories
   # })
    if request.method == "POST":
        form = AddListingForm(request.POST)
        if form.is_valid():
            item = Listing(owner = User.objects.get(id=request.user.id),
                           title=form.cleaned_data['title'],
                           description=form.cleaned_data['description'],
                           start_bid=form.cleaned_data['start_bid'],
                           image_url=form.cleaned_data['image_url'],
                           category=form.cleaned_data['category'])
            item.save()
            return render(request, "auctions/listing.html", {
                    "message":"Added with success"
            }) 
    else:
        form = AddListingForm()

    return render(request, "auctions/listing.html", {
                  "form":form
    })


def item_view(request, item_id):
    item = Listing.objects.get(id=item_id)
    on_list = False
    message = ""
    if not item:
        return render("auctions/index.html", {
            "message": f"Item {item_id} does not exist.",
        })

    comments = Comments.objects.all().filter(listing_id=item_id)
    comment_form = AddCommentForm()
    if item.open == False:
        print("Auction closed")
        if item.current_bid.bidder != request.user:
            message = "Auction closed";
            bids = Bids.objects.all().filter(bidder_id=request.user.id)
            print(bids)
            if bids:
                message = f"{message}. You were out bid."
        else:
            message = "Congratulations, You won this auction!"
    
    if request.method == "POST":
        item.open = False
        item.save()
        return HttpResponseRedirect(reverse("index"))

    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        watchlist = user.user_watchlist.all()

        if watchlist.filter(id=item_id).exists():
            on_list = True
        
        
    return render(request, "auctions/item.html", {
        "item": item,
        "on_list": on_list,
        "message": message,
        "comment_form":comment_form,
        "comments":comments
    })

@login_required
def comments_view(request, item_id):
    comment_form = AddCommentForm(request.POST)
    print(comment_form)
    if request.method == "POST":
        if comment_form.is_valid():
            comment = Comments(user=request.user, listing=Listing.objects.get(id=item_id),
                               comment = comment_form.cleaned_data["comment"])
            comment.save()
    return HttpResponseRedirect(reverse("item", args=[item_id,]))

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
