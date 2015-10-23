from django.shortcuts import render
from django.http import HttpResponse, QueryDict
import json
from models import *
import time
from django.contrib.auth import authenticate, login
from django import forms
from django.core.exceptions import ValidationError

    # Use this code if the POST request sends parameters
    # post = request.POST
    # Use this code if the POST request sends a JSON instead of parameters
    # post = QueryDict('', mutable=True)
    # post.update(json.loads(request.body))

def check_empty(fields, post, errors):
    for field in fields:
        field = post.get('field', '')
        if not field:
            errors.append('field must be non-empty')
    return errors


def home(request):
    return render(request, 'static/landing.html', context={})

def create_user(request):
    assert request.method == 'POST', 'api/user/create requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    username = post.get('username', '')
    if not username:
        errors.append('username must be non-empty')
    elif User.objects.filter(username=username).exists():
        errors.append('username already exists')
    password = post.get('password', '')
    if not password:
        errors.append('password must be non-empty')
    user_type = post.get('user_type', '')
    if user_type not in ['merchant', 'customer']:
        errors.append('user_type must be either merchant or customer')
    email = post.get('email', '')
    if not email:
        errors.append('email must be non-empty')
    picture = post.get('email', 'images/default_user_image') # Make this default
    first_name = post.get('first_name', '') # Optional
    last_name = post.get('last_name', '') # Optional
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    try:
        new_user = User(username=username, password=password, email=email,
                        first_name = first_name, last_name = last_name)
        new_user.full_clean()
        new_user.save()
        new_user_info = UserInfo(user=new_user, user_type=user_type, picture=picture)
        new_user_info.full_clean()
        new_user_info.save()
    except ValidationError as e:
        errors.append(e)
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    reponse = {
               'status': 200,
               'username': username,
               'user_type': user_type,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')


def log_in(request):
    # Log in should be a POST request because it requires sending a username and
    # and password through the body and not the url
    assert request.method == 'POST', 'api/user/login requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    username = post.get('username', '')
    if not username:
        errors.append('username must be non-empty')
    password = post.get('password', '')
    if not password:
        errors.append('password must be non-empty')
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    current = authenticate(username=username, password=password)
    if current is not None:
        if user.is_active:
            login(request, login)
            return render(request, 'static/landing.html', context={})
        else:
            errors.append('user is not active')
            reponse = {
                       'status': 400,
                       'errors': errors,
                      }
            return HttpResponse(json.dumps(reponse), content_type='application/json')
    else:
        errors.append('invalid username and password combination')
        reponse = {
                   'status': 200,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')

def create_store(request):
    assert request.method == 'POST', 'api/create/inventory requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    name = post.get('userID', '')
    try:
        userID = int(userID)
        user = User.objects.get(id=userID)
    except ValueError:
        userID = None
        errors.append('userID must be an integer')
    if not userID:
        errors.append('userID must be non-empty')
    name = post.get('name', '')
    # address_street = post.get('address_street', '')
    # address_city = post.get('address_city', '')
    # address_state = post.get('address_state', '')
    # address_zip = post.get('address_zip', '')

    # If using the address format
    address = post.get('address', '').split('\n')
    address_street = address[0]
    address_city = address[1]
    address_state = address[2]
    address_zip = address[3]

    phone_number = post.get('phone_number', '')
    description = post.get('description', '')
    picture = post.get('picture', '')
    fields = [
              'name',
              'address_street',
              'address_city',
              'address_state',
              'address_zip',
              'phone_number',
              # 'description',
             ]
    errors = check_empty(fields)
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    try:
        new_store = Store(user = user, name=name, description=description, picture=picture,
                          address_street=address_street, address_city=address_city,
                          address_state = address_state, address_zip = address_zip,
                          phone_number=phone_number)
        new_store.full_clean()
        new_store.save()
    except ValidationError as e:
        errors.append(e)
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    reponse = {
               'status': 200,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

def create_inventory(request):
    assert request.method == 'POST', 'api/create/inventory requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    storeID = post.get('storeID', '')
    try:
        storeID = int(storeID)
    except ValueError:
        storeID = None
        errors.append('storeID must be an integer')
    if not storeID:
        errors.append('storeID must be non-empty')
    elif not Store.objects.filter(id=storeID).exists():
        errors.append('invalid storeID')
    elif Inventory.objects.filter(store_id=storeID).exists():
        errors.append('store already has an inventory')
    else:
        store = Store.objects.get(id=storeID)
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    try:
        new_inventory = Inventory(store=store)
        new_inventory.save()
    except ValidationError as e:
        errors.append(e)
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    reponse = {
               'status': 200,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')


def create_item(request):
    assert request.method == 'POST', 'api/create/inventory requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    inventoryID = post.get('inventoryID', '')
    try:
        inventoryID = int(inventoryID)
    except ValueError:
        inventoryID = None
        inventory = None
        errors.append('inventoryID must be an integer')
    if not inventoryID:
        errors.append('inventoryID must be non-empty')
        store = None
    elif not Inventory.objects.filter(id=inventoryID).exists():
        errors.append('invalid inventoryID')
        inventory = None
        store = None
    else:
        inventory = Inventory.objects.get(id=inventoryID)
        store = inventory.store
    name = post.get('name', '')
    if not name:
        errors.append('name must be non-empty')
    description = post.get('description', '')
    price = post.get('price', '')
    try:
        price = float(price)
    except ValueError:
        price = None
        errors.append('price must be a number')
    if (price is not None) and price < 0.0:
        errors.append('price must be a positive number')
    picture = post.get('picture', '')
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    if Item.objects.filter(name=name, inventory_id=inventoryID).exists():
        errors.append('items in inventory must have unique names')
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')        
    try:
        new_item = Item(store=store, inventory=inventory, name=name,
                        description=description, price=price, picture=picture)
        new_item.full_clean()
        new_item.save()
    except ValidationError as e:
        errors.append(e)
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    reponse = {
               'status': 200,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

def add_inventory(request):
    return create_item(request)

def edit_item(request):
    assert request.method == 'POST', 'api/create/inventory requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    itemID = post.get('inventoryID', '')
    try:
        itemID = int(itemID)
    except ValueError:
        itemID = None
        errors.append('itemID must be an integer')
    if not itemID:
        errors.append('itemID must be non-empty')
    elif not Item.objects.filter(id=itemID).exists():
        errors.append('invalid itemID')
    else:
        current_item = Item.objects.get(id=itemID)
    name = post.get('name', '')
    description = post.get('description', '')
    price = post.get('price', '')
    if price:
        try:
            price = float(price)
            if price < 0.0:
                errors.append('price must be a positive number')
        except ValueError:
            price = None
            errors.append('price must be a number')
    picture = post.get('picture', '')
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    not_unique = Item.objects.filter(name=name, inventory_id=current_item.inventory.id).exists()
    if (current_item.name != name) and not_unique:
        errors.append('items in inventory must have unique names')
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')   
    try:
        if name:
            current_item.name = name
        if description:
            current_item.description = description
        if picture:
            current_item.picture = picture
        if price:
            current_item.price = price
        current_item.full_clean()
        current_item.save()
    except ValidationError as e:
        errors.append(e)
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    reponse = {
               'status': 200,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

def edit_inventory(request):
    return edit_item(request)


def getZip(address):
    return address.split('\n')[4]

# Basic version of search checks if item name contains
def search_items(request):
    assert request.method == 'GET', 'search requires a GET request'
    errors = []
    get = request.GET
    query = get.get('query', '')
    if not query:
        errors.append('query must be non-empty')
    location = get.get('query', '')
    if len(locations.split('\n')) != 5:
        errors.append('location incorrectly formatted')
        address_zip = '!!!!!'
    else:
        address_zip = getZip(location)
    if len(address_zip) != 5:
        errors.append('zip code must be 5 characters')
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    items = Item.objects.filter(name__icontains=query, store__address_zip=address_zip)
    if not items.exists():
        errors.append('items in inventory must have unique names')
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    retrieve = ['store',
                'inventory',
                'name',
                'description',
                'price',
                'picture',
                'store__user',
                'store__name',
                'store__address_street',
                'store__address_city',
                'store__address_state',
                'store__address_zip',
                'store__phone_number',
                'store__description',
                'store__picture',
                ]  
    json_items = [i for i in items.values(retrieve)]
    reponse = {
               'status': 200,
               'errors': json_items,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')