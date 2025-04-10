from django.urls import path
from .views import signUp, login, getUser, get_note, save_note, get_subscription, create_subscription, assign_sub, get_UserSubscriptions, get_spec_usersub

from graphene_django.views import GraphQLView

urlpatterns = [
    path('get',getUser, name='get_user'),
    path('signup',signUp, name='signup_user'),
    path('login',login, name='login_user'),

    path('notes/get/<int:pk>', get_note, name='get_notes'),
    path('notes/save/<int:pk>', save_note, name='save_notes'),

    path('subscription/create', create_subscription, name='create_subscrioption'), #create subscription
    path('subscription/get', get_subscription, name='get_subscription'), #get all available subscriptions
    path('subscription/usersub/get', get_UserSubscriptions, name='get_usersubscription'), #get all user subscriptions
    path('subscription/assign/<int:pk>',assign_sub, name='assign_subscription'), #assign subscription
    path('subscription/get/<int:pk>',get_spec_usersub, name='get_specific_user_subscription'), #get specific user subscription

    path('graphql/', GraphQLView.as_view(graphiql=True)),

]