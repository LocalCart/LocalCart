from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=16)
    picture = models.CharField(max_length=128, null=True) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Store(models.Model):

    # inventoryID = models.ForeignKey(Inventory)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=64)
    address_street = models.CharField(max_length=64)
    address_city = models.CharField(max_length=32)
    address_state = models.CharField(max_length=32)
    address_zip = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=16)
    description = models.CharField(max_length=4096, default="Good Store") # Allowed to be empty?
    picture = models.CharField(max_length=128, default="images/default_user_image", null=True) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add hours



class Inventory(models.Model):

    store = models.ForeignKey(Store)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Item(models.Model):

    store = models.ForeignKey(Store)
    inventory = models.ForeignKey(Inventory)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=4096) # Allowed to be empty? NO
    price = models.FloatField(max_length=4096)
    picture = models.CharField(max_length=128) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reviews(models.Model):

    user = models.ForeignKey(User)
    store = models.ForeignKey(Store)
    itemID = models.ForeignKey(Item)
    rating = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=4096, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class CartList(models.Model):

    user = models.ForeignKey(User)
    name = models.CharField(max_length=64)



class ListItem(models.Model):

    cartlist = models.ForeignKey(CartList)
    item = models.ForeignKey(Item, null=True)
    item_name = models.CharField(max_length=64)
    list_position = models.PositiveSmallIntegerField(unique=True)



def create_new_user(username, password, email, first_name, last_name, user_type, picture):
    """
    Assume all necessary info is correctly filled in, but check to see if user already exists.
    Create a new user with given information.
    First and last names are optional (can be empty).
    """
    if User.objects.filter(username=username).exists():
        return None
    new_user = User.objects.create_user(username=username, password=password, email=email, 
        first_name = first_name, last_name = last_name)
    new_user.full_clean()
    new_user.save()
    new_user_info = UserInfo(user=new_user, user_type=user_type, picture=picture)
    new_user_info.full_clean()
    new_user_info.save()
    return new_user_info