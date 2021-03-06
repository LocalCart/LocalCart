from django.db import models
from django.contrib.auth.models import User
import json
import urllib
from time import sleep
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
import re
from django.db.models import Q

default_image = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/PjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+PGRlZnMvPjxyZWN0IHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgZmlsbD0iI0VFRUVFRSIvPjxnPjx0ZXh0IHg9IjEzLjQ2MDkzNzUiIHk9IjMyIiBzdHlsZT0iZmlsbDojQUFBQUFBO2ZvbnQtd2VpZ2h0OmJvbGQ7Zm9udC1mYW1pbHk6QXJpYWwsIEhlbHZldGljYSwgT3BlbiBTYW5zLCBzYW5zLXNlcmlmLCBtb25vc3BhY2U7Zm9udC1zaXplOjEwcHQ7ZG9taW5hbnQtYmFzZWxpbmU6Y2VudHJhbCI+NjR4NjQ8L3RleHQ+PC9nPjwvc3ZnPg=="

class UserInfo(models.Model):
    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=16)
    picture = models.CharField(max_length=4096, default=default_image, null=True) # A url
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

    user = models.OneToOneField(User)
    name = models.CharField(max_length=64)
    address_street = models.CharField(max_length=64)
    address_city = models.CharField(max_length=32)
    address_state = models.CharField(max_length=32)
    address_zip = models.CharField(max_length=16)
    phone_number = models.CharField(max_length=16)
    description = models.CharField(max_length=4096, blank=True)
    picture = models.CharField(max_length=4096, default=default_image, null=True) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        new_inventory = Inventory(store=new_store)
        new_inventory.full_clean()
        new_inventory.save()
        return new_store

    def edit_store(self, name, address_street, address_city, address_state, address_zip,
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
        items = Item.objects.filter(inventory=inventory).order_by('created_at')
        items_in_array = []
        i = 0
        for item in items:
            i += 1
            item_in_dic = {
                           "itemID": item.id,
                           "storeName": item.store.name,
                           "name": item.name,
                           "description": item.description,
                           "price": item.price,
                           "picture": item.picture,
                           "index": i
                          }
            items_in_array.append(item_in_dic)
        return False, items_in_array


class Item(models.Model):

    store = models.ForeignKey(Store)
    inventory = models.ForeignKey(Inventory)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=4096) # Allowed to be empty? NO
    price = models.FloatField(max_length=4096)
    picture = models.CharField(max_length=4096, default=default_image, null=True) # A url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('inventory', 'name')


    @staticmethod
    def basic_search_items(query, location):
        errors = []
        if len(location.strip()) == 0:
            errors.append('location empty')
            address_zip = '!!!!!'
        else:
            address_zip = location.split()[-1]
        if len(address_zip) != 5:
            errors.append('zip code must be 5 characters')
        items = Item.objects.filter(name__icontains=query, store__address_zip=address_zip)
        return items, errors


    @staticmethod
    def search_items(query, location, location_coord=None, keep_n=20, max_dist=40000):
        errors = []
        if len(query.strip()) == 0:
            errors.append('query empty')
        if len(location.strip()) == 0:
            errors.append('location empty')
        elif location_coord is None:
            location_coord = lat_lon(location)
            if location_coord is None:
                errors.append('location not found')
        counter = 1
        items = []
        if len(errors) == 0:
            all_relevant_items = Item.relevant_items(query)
            all_relevant_values = all_relevant_items.values('id', 'price', 'store__address_street',
                                                            'store__address_city', 'store__address_state',
                                                            'store__address_zip')
            for value_dict in all_relevant_values:
                address = [
                           value_dict['store__address_street'],
                           value_dict['store__address_city'],
                           value_dict['store__address_state'],
                           value_dict['store__address_zip'],
                          ]
                value_dict['address'] = ' '.join(address)
            relevant_chunks = []
            for i in xrange(0, len(all_relevant_values), 100):
                relevant_chunks.append(all_relevant_values[i:i+100])
            pause = False
            ids = []
            prices = []
            destinations = []
            distances = []
            for chunk in relevant_chunks:
                # Google limits 100 elements per 10 seconds
                if pause:
                    sleep(10)
                pause = True
                ids += [value_dict['id'] for value_dict in chunk]
                prices += [value_dict['price'] for value_dict in chunk]
                destinations += [value_dict['address'] for value_dict in chunk]
                distances += one_to_many_distance_matrix(location, destinations)
            zipped = zip(distances, ids, prices, destinations)
            zipped = filter(lambda x: x[0] < max_dist, zipped)
            heuristics = map(Item.heur_func, zipped)
            sorted_tuples = sorted(heuristics)
            final_ids = [s[1] for s in sorted_tuples]
            final_ids = final_ids[:keep_n]
            items_qs = Item.objects.filter(id__in=final_ids)
            items_dict = dict([(i.id, i) for i in items_qs])
            items = [items_dict[fid] for fid in final_ids]
        return items, errors

    @staticmethod
    def heur_func(x):
        distance = x[0]
        curr_id = x[1]
        price = x[2]
        price_adder = 0.01
        if price > 1.00:
            price_adder = 0.10
        if price > 10.00:
            price_adder = 1.00
        heur = ((distance + 1) * ((price + price_adder) ** 0.5))
        # print(distance, price, heur, curr_id, x[3]) #Print for debugging heuristic
        return (heur, curr_id)


    # Returns all items that have names and descriptions that contain all terms in the query
    @staticmethod
    def relevant_items(query):
        search_terms = query.replace('"', '').split()
        quoted_terms = re.findall(r'"([^"]*)"', query)
        search_terms += quoted_terms
        combined_query = None
        for s_term in search_terms:
            if combined_query is None:
                combined_query = (Q(name__icontains=s_term) | Q(description__icontains=s_term))
            else:
                combined_query &= (Q(name__icontains=s_term) | Q(description__icontains=s_term))
        return Item.objects.filter(combined_query)

    @staticmethod
    def get_item(item_id):
        if not Item.objects.filter(id=item_id).exists():
            return True, {}
        item = Item.objects.get(id=item_id)
        item_in_dic = {
        "itemID": item.id,
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
    item = models.ForeignKey(Item, null=True, blank=True)
    store = models.ForeignKey(Store)
    rating = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=4096, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_new_review(user, item, store, rating, text):
        new_review = Review(user=user, item=item, store=store, 
                                rating=rating, text=text)
        new_review.full_clean()
        new_review.save()
        return new_review

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
        except (ValidationError, IntegrityError) as e:
            ListItem.objects.filter(cartlist=current_list).delete()
            ListItem.objects.filter(cartlist=temp).update(cartlist=current_list)
            temp.delete()
            return 'VE'
        temp.delete()
        return 'Success'

    @staticmethod
    def resolve_list(listID, location):
        errors = []
        location_coord = lat_lon(location)
        if location_coord is None:
            errors.append('location not found')
        elif not CartList.objects.filter(id=listID).exists():
            errors.append('Invalid listID')
        else:
            current_list = CartList.objects.get(id=listID)
            list_items = ListItem.objects.filter(cartlist=current_list, item__isnull=True)
            for li in list_items:
                li_items, li_errors = Item.search_items(query=li.item_name, location=location, 
                                                        location_coord=location_coord,
                                                        keep_n=1, max_dist=40000)
                if len(li_errors) > 0:
                    errors.append('Item ' + li.item_name + ' was not successfully resolved')
                elif len(li_items) == 0:
                    errors.append('Item ' + li.item_name + ' could not be found locally')
                else:
                    try:
                        li.item = li_items[0]
                        li.item_name = li_items[0].name
                        li.full_clean()
                        li.save()
                    except (ValidationError, IntegrityError) as e:
                        errors.append('Item ' + li.item_name + ' caused an error')
        return errors



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
        if CartList.objects.filter(id=listID).exists():
            current_list = CartList.objects.get(id=listID)
            return CartList.delete_list(current_list.user.username, current_list.name)
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
                    map_dict[store.name]['positions'].append(counter)
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
                    curr_entry['positions'] = [counter]
                    map_dict[store.name] = curr_entry
        map_markers = []
        for store_name in map_dict.keys():
            store_dict = map_dict[store_name]
            if store_dict['location']:
                pin = store_name + ' (' + ', '.join([str(x) for x in store_dict['positions']]) + ')'
                map_markers.append({
                                    'pin_name': pin,
                                    'position': min(store_dict['positions']),
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

        item_list = []
        counter = 0
        for list_item in list_items:
            if list_item.item:
                counter += 1
                current_item = list_item.item
                json_item =  {
                              "type": "id",
                              "storeName": current_item.store.name,
                              "name": current_item.name,
                              "description": current_item.description,
                              "price": current_item.price,
                              "picture": current_item.picture,
                              "itemID": current_item.id,
                              "mapIndex": counter,
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
    list_position = models.PositiveSmallIntegerField()
    

def lat_lon(address):
    gm_url = 'http://maps.googleapis.com/maps/api/geocode/json?'
    full_url = gm_url + urllib.urlencode({'address': address})
    resp = json.loads(urllib.urlopen(full_url).read())
    if resp['results']:
        loc = resp['results'][0]['geometry']['location']
        return loc['lat'], loc['lng']
    else:
        return None

def one_to_many_distance_matrix(origin, destinations):
    gm_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    full_url = gm_url + urllib.urlencode({'origins': origin, 'destinations': '|'.join(destinations)})
    if len(full_url) < 2000:
        resp = json.loads(urllib.urlopen(full_url).read())
        if resp['rows']:
            elements = resp['rows'][0]['elements']
            distances = []
            for elem in elements:
                if elem['status'] == 'OK':
                    distances.append(elem['distance']['value'])
                else:
                    distances.append(100000000)
            return distances
        else:
            return None
    else:
        n = len(destinations)
        left = destination[0:n//2]
        right = destination[n//2:]
        left_dists = one_to_many_distance_matrix(origin, left)
        right_dists = one_to_many_distance_matrix(origin, right)
        if (left_dists is None) or (right_dists is None):
            return None
        else:
            return left_dists + right_dists
