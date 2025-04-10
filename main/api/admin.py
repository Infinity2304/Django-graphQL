from django.contrib import admin

from .models import Subscription, UserSubscription, User

# Register your models here.
admin.site.register([Subscription, UserSubscription, User])
