from django.db import models
from django.contrib.auth.models import User



class UserInfo(models.Model):
    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=16)
    picture = models.CharField(max_length=128, null=True) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
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

    @staticmethod
    def edit_user_info(username, first_name=None, last_name=None, email=None, password=None, picture=None):
        """
        Assume all necessary info is correctly filled in, but check to see if username exists.
        Edit user info with information given.
        All inputs can be None except username.
        """
        if not User.objects.filter(username=username).exists():
            return None
        current_user = User.objects.get(username=username)
        current_user_info = UserInfo.objects.get(user__username=username)
        if first_name is not None:
            current_user.first_name = first_name
        if last_name is not None:
            current_user.last_name = last_name
        if email is not None:
            current_user.email = email
        if password is not None:
            current_user.set_password(password)
        current_user.save()
        if picture is not None:
            current_user_info.picture = picture
            current_user_info.save()
        return current_user_info.user_type




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

    class Meta:
        unique_together = ('inventory', 'name')


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

    class Meta:
        unique_together = ('user', 'name')

    @staticmethod
    def temporary_storage(user):
        temp_name = 'temporary_storage'
        while CartList.objects.filter(user=user, name=temp_name).exists():
            temp_name += '@'
            if len(temp_name) > 64:
                import random
                import string
                temp_name = random.sample(string.letters)
        temp = CartList(user=user, name=temp_name)
        return temp

    @staticmethod
    def create_new_list(username, name):
        if not User.objects.filter(username=username).exists():
            return None
        new_list = CartList(user=User.objects.get(username=username), name=name)
        new_list.full_clean()
        new_list.save()
        return new_list

    @staticmethod
    def refill_list(listID, contents):
        if not CartList.objects.filter(id=listID).exists():
            return None
        current_list = CartList.objects.get(id=listID)
        items = []
        item_names = []
        for content_item in contents:
            if content_item['type'] == 'id':
                item = Item.objects.get(id=content_item['name'])
                items.append(item)
                item_names.append(item.name)
            else:
                items.append(None)
                item_names.append(content_item['name'])
        temp = CartList.temporary_storage()
        ListItem.objects.filter(cartlist=current_list).update(cartlist=temp)
        try:
            for i in range(0, len(contents)):
                new_list_item = ListItem(cartlist=current_list, item=items[i], 
                                         item_name=item_names[i], list_position=i)
                new_list_item.save()
        except ValidationError as e:
            ListItem.objects.filter(cartlist=temp).update(cartlist=current_list)
            return 'VE'
        return 'Success'


    @staticmethod
    def empty_list(username, name):
        if not CartList.objects.filter(user__username=username, name=name).exists():
            return None
        current_list = CartList.objects.get(user__username=username, name=name)
        ListItem.objects.filter(cartlist=current_list).delete()
        return 'Success'

    @staticmethod
    def delete_list(username, name):
        if CartList.empty_list(username, name) is not None:
            CartList.objects.filter(user__username=username, name=name).delete()
            return 'Success'
        else:
            return None
        

class ListItem(models.Model):

    cartlist = models.ForeignKey(CartList)
    item = models.ForeignKey(Item, null=True)
    item_name = models.CharField(max_length=64)
    list_position = models.PositiveSmallIntegerField(unique=True)

