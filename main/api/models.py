from django.db import models
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.

class Subscription(models.Model):
    service = models.CharField(max_length=20, unique=True)
    time = models.IntegerField(default=0)

class UserSubscription(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    expiry_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_expiry(self):
        duration_days = self.subscription.time
        self.expiry_time = self.created_at + timedelta(days=duration_days)
        self.save()

    class Meta:
        unique_together = ('user', 'subscription')



class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.pk is None and self.password: #only hash the password on creation
            self.set_password(self.password)
            self.password = self.password #reset the password field to the new hashed password.
        super().save(*args, **kwargs)

class Note(models.Model):
    userId = models.ForeignKey("api.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    note = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
