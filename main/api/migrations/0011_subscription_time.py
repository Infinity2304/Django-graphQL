# Generated by Django 5.1.7 on 2025-03-21 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_user_subscriptions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='time',
            field=models.IntegerField(default=0),
        ),
    ]
