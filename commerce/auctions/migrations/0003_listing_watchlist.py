# Generated by Django 4.1.7 on 2023-04-01 15:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_imageurl_listing_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='listing_watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
