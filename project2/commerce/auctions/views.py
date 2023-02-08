from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Comment, Bid, Auction

# forms

class NewListingForm(forms.ModelForm): # based on Auction model
    class Meta:
        model = Auction
        fields = ['title', 'category', 'image', 'description', 'price']

# main chunk

def index(request):
    return render(request, "auctions/index.html", {
        "listings": reversed(Auction.objects.all())
    })

def listing(request, name):
    auction = Auction.objects.get(title=name)
    if auction is None:
        raise Http404("Page not found")

    message = ""
    if request.user == auction.highest_bid.user:
        if auction.isclosed:
            message = "you've won this auction"
        else:
            message = "you're the highest bidder"

    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        elif "check" in request.POST:
            if auction in request.user.watchlist.all():
                request.user.watchlist.remove(auction)
            else:
                request.user.watchlist.add(auction)
        elif "bid" in request.POST:
            bid=float(request.POST["bid"])
            if bid<=auction.price or bid>=1000000:
                message = "invalid bid"
            else:
                auction.price = bid
                auction.highest_bid.delete()
                auction.save()
                Bid(user=request.user, auction=auction).save()
                message = "bid placed succesfuly"
        elif "comment" in request.POST:
            auction.comments.create(user=request.user, comment=request.POST["comment"]) # adding to a manytomany field using .create() or .add() and doesnt need saving
        else:
            auction.isclosed = 1
            auction.save()
            #auction.highest_bid.user.watchlist.add(auction)
            return HttpResponseRedirect(reverse("index"))

    if auction.user == auction.highest_bid.user:
        message = "no bids yet"

    return render(request, "auctions/listing.html",{
        "listing":   auction,
        "message":   message,
        "isowner":   request.user == auction.user,
        "comments":  reversed(auction.comments.all()),
        "watchlist": request.user.watchlist.all()
    })

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": reversed(request.user.watchlist.all())
    })

@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            auction =  form.save(commit=False)
            auction.user = request.user
            auction.save()
            Bid(user=request.user, auction=auction).save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user ipython manage.py makemigrationsn
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

    return render(request, "auctions/register.html")