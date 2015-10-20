from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    userID = models.ForeignKey(User)
    user_type = models.CharField(max_length=16)
    picture = models.CharField(max_length=128, null=True) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Store(models.Model):

    # inventoryID = models.ForeignKey(Inventory)
    userID = models.ForeignKey(User)
    name = models.CharField(max_length=64)
    address_street = models.CharField(max_length=64)
    address_city = models.CharField(max_length=32)
    address_state = models.CharField(max_length=32)
    address_zip = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=16)
    description = models.CharField(max_length=4096, null=True) # Allowed to be empty?
    picture = models.CharField(max_length=128, null=True) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add hours



class Inventory(models.Model):

    storeID = models.ForeignKey(Store)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Item(models.Model):

    storeID = models.ForeignKey(Store)
    inventoryID = models.ForeignKey(Inventory)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=4096, null=True) # Allowed to be empty?
    price = models.FloatField(max_length=4096)
    picture = models.CharField(max_length=128, null=True) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reviews(models.Model):

    userID = models.ForeignKey(User)
    storeID = models.ForeignKey(Store)
    itemID = models.ForeignKey(Item)
    rating = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=4096, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class List(models.Model):

    userID = models.ForeignKey(User)
    name = models.CharField(max_length=64)



class ListItem(models.Model):

    listID = models.ForeignKey(List)
    itemID = models.ForeignKey(Item, null=True)
    item_name = models.CharField(max_length=64)
    list_position = models.PositiveSmallIntegerField(unique=True)

