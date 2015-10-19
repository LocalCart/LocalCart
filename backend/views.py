from django.shortcuts import render
from django.http import HttpResponse, QueryDict
import json
from models import *
import time
from django.contrib.auth import authenticate, login
from django import forms
from django.core.exceptions import ValidationError


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
    post = request.POST
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
        userID = new_user.id
        new_user_info = UserInfo(userID=userID, user_type=user_type, picture=picture)
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
    assert request.method == 'POST', 'api/user/login requires a POST request'
    errors = []
    post = request.POST
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
    post = request.POST
    name = post.get('userID', '')
    try:
        userID = int(userID)
    except ValueError:
        userID = ''
        errors.append('userID must be an integer')
    if not userID:
        errors.append('userID must be non-empty')
    name = post.get('name', '')
    address_street = post.get('address_street', '')
    address_city = post.get('address_city', '')
    address_state = post.get('address_state', '')
    address_zip = post.get('address_zip', '')
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
        new_store = Store(storeID=storeID)
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
    post = request.POST
    storeID = post.get('storeID', '')
    try:
        storeID = int(storeID)
    except ValueError:
        storeID = ''
        errors.append('storeID must be an integer')
    if not storeID:
        errors.append('storeID must be non-empty')
    elif not Store.objects.filter(id=storeID).exists():
        errors.append('invalid storeID')
    elif Inventory.objects.filter(storeID=storeID).exists():
        errors.append('store already has an inventory')
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    try:
        new_inventory = Inventory(storeID=storeID)
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


def add_inventory(request):
    assert request.method == 'POST', 'api/create/inventory requires a POST request'
    errors = []
    post = request.POST
    inventoryID = post.get('inventoryID', '')

    try:
        inventoryID = int(inventoryID)
    except ValueError:
        inventoryID = ''
        errors.append('inventoryID must be an integer')
    if not inventoryID:
        errors.append('inventoryID must be non-empty')
        storeID = ''
    elif not Inventory.objects.filter(id=inventoryID).exists():
        errors.append('invalid inventoryID')
        storeID = ''
    else:
        storeID = Inventory.objects.filter(id=inventoryID)[0].storeID
    name = post.get('name', '')
    if not name:
        errors.append('name must be non-empty')
    description = post.get('description', '')
    price = post.get('price', '')
    try:
        price = float(price)
    except ValueError:
        price = ''
        errors.append('price must be a number')
    if (price != '') and price < 0.0:
        errors.append('price must be a positive number')
    picture = post.get('picture', '')
    if len(errors) > 0:
        reponse = {
                   'status': 400,
                   'errors': errors,
                  }
        return HttpResponse(json.dumps(reponse), content_type='application/json')
    try:
        new_item = Item(storeID=storeID, inventoryID=inventoryID, name=name,
                        description=description, price=price, picture=picture)
        new_item.full_clean()
        new_item.save()
    except Exception as e:
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
