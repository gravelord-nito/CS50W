from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

class Auction(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    watchlisted_users = models.ManyToManyField(User, blank=True, related_name="watchlist")
    date_created      = models.DateTimeField(auto_now_add=True)
    title             = models.CharField(max_length=32)
    category          = models.CharField(
        max_length=50,
        choices=[
            ("motors", "Motors"),
            ("electronics", "Electronics"),
            ("art", "Collectibles & Art"),
            ("clothing", "Clothing & Accessories"),
            ("business", "Business & Industrial"),
            ("home", "Home & Garden"),
            ("sport", "Sporting goods"),
            ("jewel", "Jewelry & Watches"),
            ("other", "Others"),
        ],
        default="other"
    )
    image             = models.URLField(blank=True)
    description       = models.TextField(blank=True)
    price             = models.DecimalField(max_digits=6, decimal_places=2)
    comments          = models.ManyToManyField(Comment, blank=True, related_name="auction")
    isclosed          = models.BooleanField(default=False)

class Bid(models.Model):
    user    = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bids")
    auction = models.OneToOneField(Auction, on_delete=models.CASCADE, related_name="highest_bid")