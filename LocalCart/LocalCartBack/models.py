from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.ForeignKey(User)
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
    description = models.CharField(max_length=4096, null=True) # Allowed to be empty?
    price = models.FloatField(max_length=4096)
    picture = models.CharField(max_length=128, null=True) # A url
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
