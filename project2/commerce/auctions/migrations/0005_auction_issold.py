# Generated by Django 4.1.5 on 2023-02-02 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_auction_highest_bidder_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='issold',
            field=models.BooleanField(default=False),
        ),
    ]
