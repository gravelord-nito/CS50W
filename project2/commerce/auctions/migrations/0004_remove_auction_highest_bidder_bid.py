# Generated by Django 4.1.5 on 2023-01-26 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_auction_number_of_bids_auction_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='highest_bidder',
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='highest_bid_owner', to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]