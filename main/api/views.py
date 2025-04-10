from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User,Note, Subscription, UserSubscription
from .serializer import UserSerializer, NoteSerializer, SubscriptionSerializer, UserSubscriptionSerializer
from django.db import IntegrityError

# Create your views here.

@api_view(['GET'])
def getUser(request):
    data = User.objects.all()
    serializedData = UserSerializer(data, many=True).data
    return Response(serializedData)


@api_view(['POST'])
def signUp(request):
    data = request.data
    serializedData = UserSerializer(data=data)

    if serializedData.is_valid():
        try:
            serializedData.save()
            return Response({'message':'User SignedUp'}, status=status.HTTP_201_CREATED)
            
        except IntegrityError as I:
            error_message = "Integrity Error"
            if "userName" in str(I):
                error_message = "max length exceeds"
            return Response({"error":error_message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializedData.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        data = request.data
        email = data.get("email")
        password = data.get("password")     

        if not email or not password:
            return Response({"error":"Username and Password required"},status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, email=email)

        if user.check_password(password):
            return Response({'message':'logged in'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error':'Wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except User.DoesNotExist:
        return Response({"error":"User Not Found"}, status=status.HTTP_404_NOT_FOUND)



#For Notes

@api_view(['GET'])
def get_note(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)

        notes = Note.objects.filter(userId = user.id)
        serializedData = NoteSerializer(notes, many=True).data

        return Response(serializedData)
    except User.DoesNotExist:
        return Response({'error':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def save_note(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)

        data = request.data
        data['userId'] = user.id

        serializedData = NoteSerializer(data=data)
        if serializedData.is_valid():
            serializedData.save()
            return Response({'message':'Notes saved'})
        else:
            return Response(serializedData.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_subscription(request):
    data = Subscription.objects.all()
    serializedData = SubscriptionSerializer(data, many=True).data

    return Response(serializedData)

    
@api_view(["POST"])
def create_subscription(request):
    data = request.data
    serializedData = SubscriptionSerializer(data=data)
    if serializedData.is_valid():
        serializedData.save()
        return Response({'message':'Subscription saved'})
    else:
        return Response(serializedData.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(["POST"])
def assign_sub(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error":"User not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    subscription_id = request.data.get("subscription_id") 

    if not subscription_id:
        return Response({"error": "Subscription ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try: 
        subscription = Subscription.objects.get(pk=subscription_id)
    except Subscription.DoesNotExist:
        return Response({"error":"Subscription not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        user_subscription = UserSubscription.objects.create(user=user, subscription=subscription)
        user_subscription.set_expiry()
    except IntegrityError:
        return Response({"error":"User already subscribed"})
    return Response({"message":"User Subscribed"},status=status.HTTP_202_ACCEPTED)
    

@api_view(["GET"])
def get_UserSubscriptions(request):
    data = UserSubscription.objects.all()
    serializedData = UserSubscriptionSerializer(data, many=True).data

    return Response(serializedData)

@api_view(['GET'])
def get_spec_usersub(request, pk):
    data = UserSubscription.objects.filter(user=pk)
    serializedData = UserSubscriptionSerializer(data, many=True).data
    return Response(serializedData)