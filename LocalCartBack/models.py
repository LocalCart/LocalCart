from django.db import models
from django.contrib.auth.models import User
import json
import urllib
from time import sleep


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
        return current_user_info




class Store(models.Model):

    # inventoryID = models.ForeignKey(Inventory)
    user = models.ForeignKey(User, unique=True)
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

    @staticmethod
    def get_store(store_id):
        if not Store.objects.filter(id=store_id).exists():
            return True, {}
        store = Store.objects.get(id=store_id)
        store_in_dic = {
        #"user": store.user,
        "name": store.name,
        "address_street": store.address_street,
        "address_city": store.address_city,
        "address_state": store.address_state,
        "address_zip": store.address_zip,
        "phone_number": store.phone_number,
        "description": store.description,
        "picture": store.picture
        }
        return False, store_in_dic

    @staticmethod
    def create_new_store(user, name, description, picture, address_street, address_city,
                          address_state , address_zip ,phone_number):
        """
        Assume all necessary info is correctly filled in.
        Create a new store with given information.
        description and picture are optional (can be empty).
        """
        new_store = Store(user=user, name=name, description=description, picture=picture,
                          address_street=address_street, address_city=address_city,
                          address_state = address_state, address_zip = address_zip,
                          phone_number=phone_number)
        new_store.full_clean()
        new_store.save()
        return new_store

    def edit_store(name, address_street, address_city, address_state, address_zip,
                   phone_number, description):
        if name:
            self.name = name
        if address_street:
            self.address_street = address_street
        if address_city:
            self.address_city = address_city
        if address_state:
            self.address_state = address_state
        if address_zip:
            self.address_zip = address_zip
        if phone_number:
            self.phone_number = phone_number
        if description:
            self.description = description
        self.full_clean()
        self.save()
        



class Inventory(models.Model):

    store = models.ForeignKey(Store)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_inventory(inventory_id):
        if not Inventory.objects.filter(id=inventory_id).exists():
            return True, []
        inventory = Inventory.objects.get(id=inventory_id)
        items = Item.objects.filter(inventory=inventory)
        items_in_array = []
        for item in items:
            status, item_in_dic = Item.get_item(item.id)
            items_in_array.append(item_in_dic)
        return False, items_in_array


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

    @staticmethod
    def get_item(item_id):
        if not Item.objects.filter(id=item_id).exists():
            return True, {}
        item = Item.objects.get(id=item_id)
        item_in_dic = {
        "storeName": item.store.name,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "picture": item.picture,
        }
        return False, item_in_dic

    def edit_item(self, name, description, picture, price):
        if name:
            self.name = name
        if description:
            self.description = description
        if picture:
            self.picture = picture
        if price:
            self.price = price
        self.full_clean()
        self.save()


class Review(models.Model):

    user = models.ForeignKey(User)
    store = models.ForeignKey(Store)
    item = models.ForeignKey(Item, null=True)
    rating = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=4096, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_new_review(user, item, store, rating, text):
        if item:
            new_review = Review(user=user, item=item, store=store, 
                                rating=rating, text=text)
        else:
            new_review = Review(user=user, store=store, 
                                rating=rating, text=text)
        new_review.full_clean()
        new_review.save()

    @staticmethod
    def get_review(reviewID):
        if not Review.objects.filter(id=reviewID).exists():
            return True, {}
        review = Review.objects.get(id=reviewID)
        if review.item:
            item = review.item.name
        else:
            item = ''
        review_in_dic = {
            "username": review.user.username,
            "store": review.store.name,
            "item": item,
            "rating": review.rating,
            "text": review.text,
            }
        return False, review_in_dic


    @staticmethod
    def get_store_reviews(store):
        store_reviews = Review.objects.filter(store=store, item__isnull=True)
        review_dicts = store_reviews.order_by('created_at').values('user__username', 'rating', 'text')
        review_list = []
        for review_dict in review_dicts:
            json_review = {
                            'username': review_dict['user__username'],
                            'item': '',
                            'rating': review_dict['rating'],
                            'text': review_dict['text']
                            }
            review_list.append(json_review)
        store_reviews_with_items = Review.objects.filter(store=store, item__isnull=False)
        review_dicts = store_reviews_with_items.order_by('created_at').values('user__username', 'item__name', 'rating', 'text')
        for review_dict in review_dicts:
            json_review = {
                            'username': review_dict['user__username'],
                            'item': review_dict['item__name'],
                            'rating': review_dict['rating'],
                            'text': review_dict['text']
                            }
            review_list.append(json_review)
        return review_list

    @staticmethod
    def get_item_reviews(item):
        item_reviews = Review.objects.filter(item=item)
        review_dicts = item_reviews.order_by('created_at').values('user__username', 'rating', 'text')
        review_list = []
        for review_dict in review_dicts:
            json_review = {
                            'username': review_dict['user__username'],
                            'rating': review_dict['rating'],
                            'text': review_dict['text']
                            }
            review_list.append(json_review)
        return review_list

        

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
        temp.save()
        return temp

    @staticmethod
    def create_new_list(username, name):
        if not User.objects.filter(username=username).exists():
            return None
        user = User.objects.get(username=username)
        if UserInfo.objects.get(user=user).user_type != "customer":
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
        temp = CartList.temporary_storage(current_list.user)
        ListItem.objects.filter(cartlist=current_list).update(cartlist=temp)
        try:
            for i in range(0, len(contents)):
                new_list_item = ListItem(cartlist=current_list, item=items[i], 
                                         item_name=item_names[i], list_position=i)
                new_list_item.save()
        except ValidationError as e:
            ListItem.objects.filter(cartlist=temp).update(cartlist=current_list)
            temp.delete()
            return 'VE'
        temp.delete()
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



    @staticmethod
    def delete_list_with_id(listID):
        if CartList.objects.filter(listID).exists():
            current_list = CartList.objects.get(listID)
            return delete_list(current_list.user.username, current_list.name)
        else:
            return None

    def map_list(self):
        map_dict = dict()
        items = ListItem.objects.filter(cartlist=self).order_by('list_position')
        counter = 0 # Google Maps API limits 10 geocodes per second
        for li in items:
            if counter % 10:
                sleep(1)
            if li.item:
                counter += 1
                store = li.item.store
                if store.name in map_dict.keys():
                    map_dict[store.name]['positions'].append(li.list_position)
                else:
                    address_list = [
                                    store.address_street,
                                    store.address_city,
                                    store.address_state,
                                    store.address_zip,
                                   ]
                    address = ' '.join(address_list)
                    coord = lat_lon(address)
                    curr_entry = dict()
                    curr_entry['location'] = coord
                    curr_entry['positions'] = [li.list_position]
                    map_dict[store.name] = curr_entry
        map_markers = []
        for store_name in map_dict.keys():
            store_dict = map_dict[store_name]
            if store_dict['location']:
                pin = store_name + ' (' + ', '.join(store_dict[positions]) + ')'
                map_markers.append({
                                    'pin_name': pin,
                                    'latitude': store_dict['location'][0],
                                    'longitude': store_dict['location'][1],
                                   })
        return map_markers



    @staticmethod
    def get_cartlist(listID):
        if not CartList.objects.filter(id=listID).exists():
            return True, []
        cartlist = CartList.objects.get(id=listID)
        list_items = ListItem.objects.filter(cartlist=cartlist).order_by('list_position')

        items_list = []
        for list_item in list_items:
            if list_item.item:
                current_item = list_item.item
                json_item =  {
                              "type": "id",
                              "storeName": current_item.store.name,
                              "name": item.name,
                              "description": current_item.description,
                              "price": current_item.price,
                              "picture": current_item.picture,
                              "itemID": item.id
                             }
            else:
                json_item =  {
                              "type": "name",
                              "storeName": '',
                              "name": list_item.item_name,
                              "description": '',
                              "price": '',
                              "picture": '',
                              "itemID": -1,
                             }
            item_list.append(json_item)
        return False, item_list
        

class ListItem(models.Model):

    cartlist = models.ForeignKey(CartList)
    item = models.ForeignKey(Item, null=True, default=None)
    item_name = models.CharField(max_length=64)
    list_position = models.PositiveSmallIntegerField(unique=True)

    @staticmethod
    def get_list_item(list_item_id):
        if not ListItem.objects.filter(id=list_item_id).exists():
            return True, {}
        list_item = ListItem.objects.get(id=list_item_id)
        item_in_dic = {
        #"store": item.store,
        #"inventory": item.inventory,
        "name": list_item.name,
        "list_position": list_item.list_position
        # "description": item.description,
        # "price": item.price,
        # "picture": item.picture
        }
        return False, item_in_dic

def lat_lon(address):
    gm_url = 'http://maps.googleapis.com/maps/api/geocode/json?'
    full_url = gm_url + urllib.urlencode({'address': address})
    resp = json.loads(urllib.urlopen(full_url).read())
    if resp['results']:
        loc = resp['results'][0]['geometry']['location']
        return loc['lat'], loc['lng']
    else:
        return None


