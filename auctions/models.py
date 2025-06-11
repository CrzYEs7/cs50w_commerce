from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    name = AbstractUser.username

    def __str__(self):
        return f"{self.id}: {self.name}"


class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="bidder")
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id}: {self.bidder}: {self.value}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=800)
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,  related_name="categorize")
    
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.ForeignKey(Bids, blank=True, null=True, on_delete=models.SET_NULL, related_name="current_bid")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=1)
    open = models.BooleanField(default=True)

    watchlist = models.ManyToManyField(User, blank=True, related_name="user_watchlist")

    def __str__(self):
        return f"{self.id}: {self.title} in the category: {self.category}"


class Comments(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="user")
    listing = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.CASCADE, related_name="listing")
    comment = models.CharField(max_length=600, blank=True, null=True)
