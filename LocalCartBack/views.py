from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
import json
from models import *
import time
from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned

    # Use this code if the POST request sends parameters
    # post = request.POST
    # Use this code if the POST request sends a JSON instead of parameters
    # post = QueryDict('', mutable=True)
    # post.update(json.loads(request.body))


@csrf_exempt
def home(request):
    return render(request, 'static/index.html', context={})


@csrf_exempt
def merchant_render(request):
    return render(request, 'static/merchant.html', context={})

@csrf_exempt
def register_render(request):
    return render(request, 'static/register.html', context={})

@csrf_exempt
def login_render(request):
    return render(request, 'static/login.html', context={})

@csrf_exempt
def search_render(request):
    return render(request, 'static/search.html', context={})

@csrf_exempt
def inventory_render(request):
    return render(request, 'inventory.html', context={})

@csrf_exempt
def empty_db(request):
    errors = []
    try:
        models = [
                  User, 
                  UserInfo, 
                  Store, 
                  Inventory, 
                  Item, 
                  Reviews,
                  CartList,
                  ListItem,
                  ]
        for m in models:
            m.objects.all().delete()
    except Exception as e:
        errors.append(e)
    reponse = {
               'status': 200,
               'errors': errors,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')


def check_empty(fields, post, errors):
    for field in fields:
        f = post.get(field, '')
        if not f:
            errors.append(field + ' must be non-empty')
    return errors

def return_error(errors):
    response = {
               'status': 200,
               'errors': errors,
                }
    return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def return_user(request):
    assert request.method == 'GET', 'api/user/get requires a GET request'
    errors = []
    user = request.user
    if not user.is_authenticated():
        errors.append('Not logged in')
        user_id = -1
        username = ''
    else:
        user_id = user.id
        username = user.username
    reponse = {
               'status': 200,
               'id': user_id,
               'username': username,
               'errors': errors,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')




@csrf_exempt
def create_user(request):
    assert request.method == 'POST', 'api/user/create requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    username = post.get('username', '')
    password = post.get('password', '')
    user_type = post.get('user_type', '')
    if user_type not in ['merchant', 'customer']:
        errors.append('user_type must be either merchant or customer')
    email = post.get('email', '')
    picture = post.get('picture', 'images/default_user_image') # Make this default
    fields = [
              'username',
              'password',
              'user_type',
              'email',
             ]
    errors = check_empty(fields, post, errors)
    first_name = post.get('first_name', '') # Optional
    last_name = post.get('last_name', '') # Optional
    if len(errors) == 0:
        try:
            new_user_info = UserInfo.create_new_user(username, password, email, first_name, last_name, user_type, picture)
        except ValidationError as e:
            errors.append(e)
        if not new_user_info:
            errors.append('username already exists')
    reponse = {
               'status': 200,
               'username': username,
               'user_type': user_type,
               'errors': errors,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')


@csrf_exempt
def edit_user(request):
    assert request.method == 'POST', 'api/user/change requires a POST request'
    errors = []
    user_type = ''
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    username = post.get('username', '')
    if not username:
        errors.append('username must be non-empty')
    email = post.get('email', None)
    picture = post.get('picture', None) # Make this default
    first_name = post.get('first_name', None) # Optional
    last_name = post.get('last_name', None) # Optional
    password = post.get('password', None)
    if (first_name is not None) and not first_name:
        errors.append('first_name must not be empty')
    if (last_name is not None) and not last_name:
        errors.append('last_name must not be empty')
    if (email is not None) and not email:
        errors.append('email must not be empty')
    if (password is not None) and not password:
        errors.append('password must not be empty')
    if (picture is not None) and not picture:
        picture = 'images/default_user_image'
    if len(errors) == 0:
        try:
            current_user_info = UserInfo.edit_user_info(username=username, first_name=first_name, 
              last_name=last_name, email=email, password=password, picture=picture)
        except ValidationError as e:
            errors.append(e)
        if not current_user_info:
            errors.append('username does not exist')
    if len(errors) == 0:
      response = {
               'status': 200,
               'username': username,
               'first_name': current_user_info.user.first_name,
               'last_name': current_user_info.user.last_name,
               'email': current_user_info.user.email,
               'user_type': current_user_info.user_type,
               'errors': errors,
                }
      return HttpResponse(json.dumps(response), content_type='application/json')
    else:
      return return_error(errors)

    
@csrf_exempt
def log_in(request):
    # Log in should be a POST request because it requires sending a username and
    # and password through the body and not the url
    assert request.method == 'POST', 'api/user/login requires a POST request'
    errors = []
    user_type = ''
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    username = post.get('username', '')
    if not username:
        errors.append('username must be non-empty')
    password = post.get('password', '')
    if not password:
        errors.append('password must be non-empty')
    if len(errors) == 0:
        current = authenticate(username=username, password=password)
        if current is not None:
            if current.is_active:
                login(request, current)
                user_type = UserInfo.objects.get(user__username=username).user_type
            else:
                errors.append('user is not active')
        else:
            errors.append('invalid username and password combination')
    reponse = {
               'status': 200,
               'username': username,
               'user_type': user_type,
               'errors': errors
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

@csrf_exempt
def log_out(request):
    assert request.method == 'POST', 'api/user/login requires a POST request'
    logout(request)
    return return_error([])

@csrf_exempt
def create_store(request):
    assert request.method == 'POST', 'api/store/create requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    username = post.get('username', '') ### changed to username since username is also unique
    if not User.objects.filter(username=username).exists():
        errors.append('username does not exist')
        user = None
    else:
        user = User.objects.get(username=username)
    
    name = post.get('name', '')

    # If using the address format
    address = post.get('address', '').split('\n')
    if len(address) == 5:
        address_street = address[0]
        address_city = address[2]
        address_state = address[3]
        address_zip = address[4]
    else:
        errors.append('address not correctly formatted')

    phone_number = post.get('phone_number', '')
    description = post.get('description', 'Good Store') #default
    picture = post.get('picture', 'images/default_user_image') #default
    fields = [
              'name',
              'address',
              'phone_number',
             ]
    errors = check_empty(fields, post, errors)
    if len(errors) > 0:
        return return_error(errors)
    try:
        new_store = Store.create_new_store(user=user, name=name, description=description, picture=picture,
                          address_street=address_street, address_city=address_city,
                          address_state = address_state, address_zip = address_zip,
                          phone_number=phone_number)
    except ValidationError as e:
        return return_error(errors)
    reponse = {
               'status': 200,
               'storeID': new_store.id,
               'errors': errors

              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

@csrf_exempt
def create_inventory(request):
    assert request.method == 'POST', 'api/create/inventory requires a POST request'
    errors = []
    n = 0;
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
        return return_error(errors)
    try:
        new_inventory = Inventory(store=store)
        new_inventory.save()
    except ValidationError as e:
        errors.append(e)
        return return_error(errors)
    response = {
               'status': 200,
               'inventoryID': new_inventory.id,
               'errors': errors
              }
    return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def create_item(request):
    # invetoryId, name, price, description, picture
    assert request.method == 'POST', 'api/create/inventory requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    inventoryID = post.get('inventoryID', '')
    try:
        inventoryID = int(inventoryID)
    except ValueError:
        inventoryID = None
        errors.append('inventoryID must be an integer')
    if not inventoryID:
        errors.append('inventoryID must be non-empty')
        storeID = ''
    elif not Inventory.objects.filter(id=inventoryID).exists():
        errors.append('invalid inventoryID')
        inventoryID = ''
    else:
        inventory = Inventory.objects.filter(id=inventoryID)[0]
        store = inventory.store
    name = post.get('name', '')
    if not name:
        errors.append('name must be non-empty')
    description = post.get('description', '')
    if not description:
        errors.append('description must be non-empty')
    price = post.get('price', '')
    try:
        price = float(price)
    except ValueError:
        price = None
        errors.append('price must be a number')
    if (price is not None) and price < 0.0:
        errors.append('price must be a positive number')
    picture = post.get('picture', 'pic')
    if not picture:
        errors.append('picture must be non-empty')
    if len(errors) > 0:
        return return_error(errors)
    if Item.objects.filter(name=name, inventory_id=inventoryID).exists():
        errors.append('items in inventory must have unique names')
        return return_error(errors)       
    try:
        new_item = Item(store=store, inventory=inventory, name=name,
                        description=description, price=price, picture=picture)
        new_item.full_clean()
        new_item.save()
    except ValidationError as e:
        errors.append(str(e))
        return return_error(errors)
    reponse = {
               'status': 200,
               'itemID': new_item.id,
               'errors': errors
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')
@csrf_exempt
def add_inventory(request):
    return create_item(request)
@csrf_exempt
def edit_item(request):
    assert request.method == 'POST', 'api/item/create requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    itemID = post.get('itemID', '')
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
        return return_error(errors)
    not_unique = Item.objects.filter(name=name, inventory=current_item.inventory).exists()
    if (current_item.name != name) and not_unique:
        errors.append('items in inventory must have unique names')
        return return_error(errors)
    try:

        current_item.edit_item(name, description, picture, price)
    except ValidationError as e:
        errors.append(e)
    return return_error(errors)

@csrf_exempt
def edit_inventory(request):
    return edit_item(request)

@csrf_exempt
def delete_item(request):
    assert request.method == 'POST', 'api/item/delete requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    itemID = post.get('itemID', '')
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
        Item.objects.filter(id=itemID).delete()
    reponse = {
               'status': 200,
               'errors': errors,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

def getZip(address):
    return address.split('\n')[4]

# Basic version of search checks if item name contains
@csrf_exempt
def search_items(request):
    assert request.method == 'GET', 'search requires a GET request'
    errors = []
    # get = QueryDict('', mutable=True)
    # get.update(json.loads(request.body))
    get = request.GET
    query = get.get('query', '')
    if not query:
        errors.append('query must be non-empty')
    location = get.get('location', '')
    #Line1\nLine2\nCity\nState\n94704
    if len(location.split('\n')) != 5:
        errors.append('location incorrectly formatted')
        address_zip = '!!!!!'
    else:
        address_zip = getZip(location)
    if len(address_zip) != 5:
        errors.append('zip code must be 5 characters')
    if len(errors) > 0:
        return return_error(errors)
    items = Item.objects.filter(name__icontains=query, store__address_zip=address_zip)
    if not items.exists():
        errors.append('empty query')
        return return_error(errors)

    json_items = [i for i in items.values('store', 'inventory', 'name', 'description',
                                        'price', 'picture', 'store__user', 'store__name',
                                        'store__address_street','store__address_city',
                                        'store__address_state',  'store__address_zip',
                                        'store__phone_number',  'store__description',
                                        'store__picture',)]
    reponse = {
               'status': 200,
               'items': json_items,
               'errors': errors
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

@csrf_exempt
def create_list(request):
    assert request.method == 'POST', 'api/list/create requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    username = post.get('username', '')
    if not username:
        errors.append('username must be non-empty')
    name = post.get('name', '')
    if not name:
        errors.append('name must be non-empty')
    if len(errors) == 0:
        try:
            new_list = CartList.create_new_list(username, name)
        except ValidationError as e:
            errors.append(e)
        if not new_list:
            errors.append('username does not exist or user is not a customer')
    if (len(errors) > 0):
      return return_error(errors)
    else:
      response = {
               'status': 200,
               'listID': new_list.id,
               'errors': errors,
                }
      return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
def delete_list(request):
    assert request.method == 'POST', 'api/list/delete requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    username = post.get('username', '')
    if not username:
        errors.append('username must be non-empty')
    name = post.get('name', '')
    if not name:
        errors.append('name must be non-empty')
    if len(errors) == 0:
        try:
            new_list = CartList.delete_list(username, name)
        except ValidationError as e:
            errors.append(e)
        if not new_list:
            errors.append('no list of this name exists for this username')
    return return_error(errors)


@csrf_exempt
def edit_list(request):
    assert request.method == 'POST', 'api/list/edit requires a POST request'
    errors = []
    post_data = json.loads(request.body)
    if 'listID' not in post_data.keys():
        errors.append('listID must be non-empty')
        listID = ''
    else:
        listID = post_data['listID']
        try:
            listID = int(listID)
        except ValueError:
            listID = None
            errors.append('listID must be an integer')
    contents = post_data['contents']
    for content_item in contents:
        if ('type' not in content_item.keys()) or ('name' not in content_item.keys()):
            errors.append('item must have name and type')
        else:
            if content_item['type'] == 'id':
                try:
                    content_item['name'] = int(content_item['name'])
                except ValueError:
                    errors.append('itemID references must be integers')
            elif content_item['type'] == 'name':
                content_item['name'] = str(content_item['name'])
            else:
                errors.append('item reference reference type must be "id" or "name"')
    if len(errors) == 0:
        try:
            refill = CartList.refill_list(listID, contents)
        except ValidationError as e:
            errors.append(e)
        except ObjectDoesNotExist as e:
            refill = 1
            errors.append('Invalid itemID')
        except MultipleObjectsReturned as e:
            refill = 1
            errors.append('Invalid itemID')
        if not refill:
            errors.append('Invalid listID')
        elif refill == 'VE':
            errors.append('List could not be entered into the database, reverted to previous state')
    return return_error(errors)


@csrf_exempt
def map_list(request):
    assert request.method == 'POST', 'api/list/map requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    listID = post.get('listID', '')
    try:
        listID = int(listID)
    except ValueError:
        listID = None
        errors.append('listID must be an integer')
    map_markers = []
    if len(errors) == 0:
        if not CartList.objects.filter(id=listID).exists():
            errors.append('listID is not valid')
            map_markers = []
        else:
            map_markers = CartList.objects.get(id=listID).map_list()
    reponse = {
               'status': 200,
               'map_markers': map_markers,
               'errors': errors,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')
