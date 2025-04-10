import graphene
from graphene_django import DjangoObjectType
from .models import User, UserSubscription, Subscription
from django.core.exceptions import ObjectDoesNotExist
from graphql import GraphQLError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


#Defining object types of django models
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id","email","name")

class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        fields = ("id","service","time")

class UserSubscriptionType(DjangoObjectType):
    class Meta:
        model = UserSubscription
        fields = ("id","user","subscription","expiry_time")




#CREATE data   ################################
#create user
class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        name = graphene.String(required=True)

    user = graphene.Field(UserType) #creates a user instance which will be returned after user is created

    def mutate(self, info, email, password, name): 
        try:
            validate_email(email)
        except ValidationError as e:
            raise GraphQLError(str(e))
        
        if User.objects.filter(email=email).exists():
            raise GraphQLError("email already exists")
        if not name:
            raise GraphQLError("Name is required")
        if not password:
            raise GraphQLError("Password is required")
        if len(name)>20:
            raise GraphQLError("Length of name should be less than 20")
        
        try:
            user = User(email=email, name=name)
            user.set_password(password) #calls the set_password method from django User model
            user.save()
            return {"user":user} #returns the newly created user object 1user in the instance of create user which we created earlier and second one is the newly created user
        except Exception as e:
            raise GraphQLError(str(e))
 

#create subscription    
class CreateSubscription(graphene.Mutation):
    class Arguments:
        service = graphene.String(required=True)
        time = graphene.Int(required=True)

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info, service, time):
        if Subscription.objects.filter(service=service).exists():
            raise GraphQLError("Service already exist")
        if not service:
            raise GraphQLError("service is required")
        if len(service)>20:
            raise GraphQLError("Length of service should be less than 20")
        if not time:
            raise GraphQLError("time is required")
        if time<0:
            raise GraphQLError("value of time should be positive")
        
        try:
            subscription = Subscription(service=service, time=time)
            subscription.save()
            return CreateSubscription(subscription=subscription)
        except Exception as e:
            raise GraphQLError(str(e))


#create/assign subscription 
class AssignSubscription(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        subscription_ids = graphene.List(graphene.Int, required=True)

    user_subscription = graphene.List(UserSubscriptionType)

    def mutate(self, info, user_id, subscription_ids):
        try:
            #validate user existence
            user = User.objects.get(pk=user_id)
            
            #validate and assign each subscription
            user_subscriptions = []
            for subscription_id in subscription_ids:
                try:
                    subscription = Subscription.objects.get(pk=subscription_id)

                    #check if user already subscribed
                    if UserSubscription.objects.filter(user=user, subscription=subscription).exists():
                       raise GraphQLError(f"User is already subscribed to {subscription.service} service") 

                    #assign the subscription
                    user_subscription = UserSubscription.objects.create(user=user, subscription=subscription)
                    user_subscription.set_expiry()
                    user_subscriptions.append(user_subscription)
                except Subscription.DoesNotExist:
                    raise GraphQLError(f"Subscription with ID {subscription_id} does not exist")
            
            return AssignSubscription(user_subscription=user_subscription)
        
        except User.DoesNotExist:
                raise GraphQLError("User does not exist")
    


#UPDATE data   #############################
#update user data
class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, id, name=None, email=None):
        try:
            user = User.objects.get(pk=id)
            if name:
                if len(name)>20:
                    raise GraphQLError("Length of name should be less than 20")
                user.name = name
            if email:
                try:
                    validate_email(email)
                    if User.objects.filter(email=email).exclude(pk=id).exists():
                        raise GraphQLError("email already exists")
                    user.email = email
                except ValidationError as e:
                    raise GraphQLError(str(e))
            user.save()
            return UpdateUser(user=user)
        except ObjectDoesNotExist:
            raise GraphQLError("User not found")
        
#update subscription data
class UpdateSubscription(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        service = graphene.String()
        time = graphene.Int()

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info, id, service=None, time=None):
        try:
            subscription = Subscription.objects.get(pk=id)
            if service:
                if Subscription.objects.filter(service=service).exclude(pk=id).exists():
                        raise GraphQLError("service already exists")
                subscription.service = service
            if time: 
                if time<0:
                    raise GraphQLError("value of time should be positive")
                subscription.time = time
            subscription.save()
            return UpdateSubscription(subscription=subscription)
        except ObjectDoesNotExist:
            raise GraphQLError("Subscription not found")


        
# DELETE data   ##################################
# delete user
class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id= graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, user_id):
        try:
            user = User.objects.get(pk= user_id)
            user.delete()
            return DeleteUser(success= True)
        except ObjectDoesNotExist:
            raise GraphQLError("User not found")
        
class DeleteSubscription(graphene.Mutation):
    class Arguments:
        subscription_id= graphene.Int(required=True)
    
    success = graphene.Boolean()

    def mutate(self, info, subscription_id):
        try:
            subscription = Subscription.objects.get(pk=subscription_id)
            subscription.delete()
            return DeleteSubscription(success=True)
        except ObjectDoesNotExist:
            raise GraphQLError("Subscription not found")

#remove user-subscription
class RemoveUserSubscription(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        subscription_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, user_id, subscription_id):
        try:
            if not User.objects.filter(pk=user_id).exists():
                raise GraphQLError("User does not exist")
            
            if not Subscription.objects.filter(pk=subscription_id).exists():
                raise GraphQLError("Subscription does not exist")
            
            user_subscription = UserSubscription.objects.get(user_id=user_id, subscription_id=subscription_id)
            user_subscription.delete()
            return RemoveUserSubscription(success=True)
        except ObjectDoesNotExist:
            raise GraphQLError("user is not subscribed to the given subscription")


#mutation class is used to create/update an object in the database
class Mutation(graphene.ObjectType):
    #create mutations
    create_user = CreateUser.Field()
    create_subscription = CreateSubscription.Field()
    assign_subscription = AssignSubscription.Field()
    #update mutations
    update_user = UpdateUser.Field()
    update_subscription = UpdateSubscription.Field()
    #delete mutations
    remove_user_subscription = RemoveUserSubscription.Field()
    delete_user = DeleteUser.Field()
    delete_subscription = DeleteSubscription.Field()


    
#query class is used to fetch/read the data/objects from the database
class Query(graphene.ObjectType):
    all_users_info = graphene.List(UserType)
    all_subscriptions_info = graphene.List(SubscriptionType)
    all_usersubscriptions_info = graphene.List(UserSubscriptionType)
    spec_user = graphene.List(
        UserType,
        user_id=graphene.Int(),
        name=graphene.String(),
        email=graphene.String()
    )
    spec_subscription = graphene.List(
        SubscriptionType,
        subscription_id=graphene.Int(),
        service=graphene.String(),
    )
    spec_user_subscriptions = graphene.List(
        UserSubscriptionType,
        user_id=graphene.Int(),
        subscription_id =graphene.Int()

    )

    #To get all users
    def resolve_all_users_info(root, info):
        return User.objects.all()

    #To get all subscriptions
    def resolve_all_subscriptions_info(root, info):
        return Subscription.objects.all()

    #To get all user-subscription
    def resolve_all_usersubscriptions_info(root, info):
        return UserSubscription.objects.all()
    

    #To get specific user with filter
    def resolve_spec_user(root, info, user_id=None, name=None, email=None):
        users = User.objects.all()
        if user_id:
            users = users.filter(id=user_id)
        if name:
            users = users.filter(name__icontains=name)
        if email:
            users = users.filter(email__icontains=email)
        return users
    
    #To get specific subscription with filter
    def resolve_spec_subscription(root, info, subscription_id=None, service=None):
        subscription = Subscription.objects.all()
        if subscription_id:
            subscription = subscription.filter(id=subscription_id)
        if service:
            subscription = subscription.filter(service__icontains=service)
        return subscription
    
    #To get specific user-subscription with filter
    def resolve_spec_user_subscriptions(root, info, user_id=None, subscription_id=None): 
        user_subscription = UserSubscription.objects.all()
        if user_id:
            user_subscription = user_subscription.filter(user_id=user_id)
        if subscription_id:
            user_subscription = user_subscription.filter(subscription_id=subscription_id)  
        return user_subscription


    
schema = graphene.Schema(query=Query, mutation=Mutation)