# Generated by Django 4.1.5 on 2023-02-08 12:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_issold_auction_isclosed_alter_bid_auction'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='watchlisted_users',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
