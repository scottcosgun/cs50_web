from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name

class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    def __str__(self):
        return f"{self.bid}"
    
class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    name = models.CharField(max_length=128)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    description = models.CharField(max_length=500)
    img_url = models.CharField(max_length=1000)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listing_watchlist")

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    user_comment = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.author}'s comment on {self.listing}"