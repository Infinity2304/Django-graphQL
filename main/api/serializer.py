from rest_framework import serializers
from .models import User, Note, Subscription, UserSubscription

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)
    class Meta:
        model = User
        fields = '__all__'

    
class NoteSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Note
        fields = '__all__'

    def get_user_email(self, obj):
        return obj.userId.email
    

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'