from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
import json
from models import *
import time
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
import tablib
from admin import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
def store_render(request):
    return render(request, 'store.html', context={})

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
                  Review,
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
    errors, user = extract_user(request, errors)
    if len(errors) > 0:
        user_id = -1
        username = ''
        user_type = 'customer'
    else:
        user_id = user.id
        username = user.username
        user_type = UserInfo.objects.get(user=user).user_type
    reponse = {
               'status': 200,
               'id': user_id,
               'username': username,
               'user_type': user_type,
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
    picture = post.get('picture', default_image) # Make this default
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
        picture = default_image
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
    errors, user = extract_user(request, errors)
    if user:
        current_user_info = UserInfo.objects.get(user=user)
        current_user_type = current_user_info.user_type
        if current_user_type != "merchant":
            errors.append('Only merchants can create stores')
    name = post.get('name', '')

    # If using the address format
    address = post.get('address', '').split('\n')
    if len(address) == 5:
        address_street = address[0]
        address_city = address[2]
        address_state = address[3]
        address_zip = address[4]
        if Store.objects.filter(address_street=address_street, address_city=address_city,
                              address_state = address_state, address_zip = address_zip).exists():
            errors.append('store already exists at this address')
    else:
        errors.append('address not correctly formatted')

    phone_number = post.get('phone_number', '')
    description = post.get('description', '') #default
    picture = post.get('picture', '') #default
    if not picture:
        picture = default_image
    fields = [
              'name',
              'address',
              'phone_number',
             ]
    errors = check_empty(fields, post, errors)
    storeID = -1
    if len(errors) == 0:
        try:
            new_store = Store.create_new_store(user=user, name=name, description=description, picture=picture,
                              address_street=address_street, address_city=address_city,
                              address_state=address_state, address_zip = address_zip,
                              phone_number=phone_number)
        except ValidationError as e:
            errors.append(e)
        else:
            storeID = new_store.id,
    reponse = {
               'status': 200,
               'storeID': storeID,
               'errors': errors
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

@csrf_exempt
def edit_store(request):
    assert request.method == 'POST', 'api/store/edit requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    storeID = post.get('storeID', '')
    try:
        storeID = int(storeID)
        store = Store.objects.get(id=storeID)
    except ValueError:
        store = None
        errors.append('storeID must be an integer')
    except ObjectDoesNotExist:
        store = None
        errors.append('Store does not exist')

    name = post.get('name', '')
    address_street = post.get('address_street', '')
    address_city = post.get('address_city', '')
    address_state = post.get('address_state', '')
    address_zip = post.get('address_zip', '')
    address = [address_street, address_city, address_state, address_zip]
    address_change = any(address)
    if (store is not None) and address_change:
        if not address_street:
            address_street = store.address_street
        elif address_street == store.address_street:
            address_change = False
        if not address_city:
            address_city = store.address_city
        elif address_city == store.address_city:
            address_change = False
        if not address_state:
            address_state = store.address_state
        elif address_state == store.address_state:
            address_change = False
        if not address_zip:
            address_zip = store.address_zip
        elif address_zip == store.address_zip:
            address_change = False
        if address_change and Store.objects.filter(address_street=address_street, address_city=address_city,
                                                    address_state=address_state, address_zip=address_zip).exists():
            errors.append('store already exists at this address')
    phone_number = post.get('phone_number', '')
    description = post.get('description', '')
    if len(errors) > 0:
        return return_error(errors)
    try:
        store.edit_store(name=name, description=description, phone_number=phone_number,
                         address_street=address_street, address_city=address_city,
                         address_state = address_state, address_zip = address_zip)
    except ValidationError as e:
        return return_error(errors)
    reponse = {
               'status': 200,
               'errors': errors
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')


@csrf_exempt
def get_store_user(request):
    errors = []
    store_info = {
                  'storeID': -1,
                  'name': '',
                  'address_street': '',
                  'address_city': '',
                  'address_state': '',
                  'address_zip': '',
                  'phone_number': '',
                  'description': '',
                  'picture': '',
                 }
    errors, user = extract_user(request, errors)
    if len(errors) == 0:
        if Store.objects.filter(user=user).exists():
            store = Store.objects.get(user=user)
        else:
            store = None
        if store:
            store_info = {
                          'storeID': store.id,
                          'name': store.name,
                          'address_street': store.address_street,
                          'address_city': store.address_city,
                          'address_state': store.address_state,
                          'address_zip': store.address_zip,
                          'phone_number': store.phone_number,
                          'description': store.description,
                          'picture': store.picture,
                         }
    response = {
               'status': 200,
               'errors': errors,
               'store': store_info,
              }
    return HttpResponse(json.dumps(response), content_type='application/json', status=200)

@csrf_exempt
def get_store(request):
    hasError = False
    retData = { 
                "status": 200,
                "errors": []
                }
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    storeID = post.get('storeID', '')
    if storeID == "":
        retData["errors"].append("storeID must be non-empty")
        hasError = True
    if not hasError:
        hasError, store = Store.get_store(storeID)
        if hasError:
            retData["errors"].append("Can't get store from storeID")
        retData["store"] = store
    return HttpResponse(json.dumps(retData), content_type='application/json', status=200)


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
def get_inventory(request):
    hasError = False
    retData = { 
                "status": 200,
                "errors": []
                }

    inventoryID = request.GET.get('inventoryID', '')    
    if inventoryID == "":
        retData["errors"].append("inventoryID must be non-empty")
        hasError = True
    if not hasError:
        hasError, inventory = Inventory.get_inventory(inventoryID)
        if hasError:
            retData["errors"].append("Can't get inventory from inventoryID")
        retData["inventory"] = inventory
    return HttpResponse(json.dumps(retData), content_type='application/json', status=200)

@csrf_exempt
def get_inventory_store(request):
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    storeID = post.get('storeID', '')
    hasError = False
    inventory_list = []
    inventoryID = -1
    if storeID == "":
        errors.append("store must be non-empty")
        hasError = True
    if not hasError:
        if not Store.objects.filter(id=storeID).exists():
          errors.append("StoreID doesn't exist")
          store = None
        else:
          store = Store.objects.get(id=storeID)
          inventory = Inventory.objects.get(store=store)
          inventoryID = inventory.id
          hasError, inventory_list = Inventory.get_inventory(inventory.id)
    response = {
       'status': 200,
       'inventoryID': inventoryID,
       'contents': inventory_list,
       'errors': errors
      }
    return HttpResponse(json.dumps(response), content_type='application/json', status=200)

@csrf_exempt
def get_user_inventory(request):
    assert request.method == 'GET', 'api/inventory/getUser requires a GET request'
    errors = []
    errors, user = extract_user(request, errors)
    inventory_list = []
    inventoryID = -1
    if not Store.objects.filter(user=user).exists():
        errors.append('user does not have inventory')
        store = None
        inventory = None
    else:
        store = Store.objects.get(user=user)
        if not Inventory.objects.filter(store=store).exists():
            errors.append('user does not have inventory')
            inventory = None
        else:
            inventory = Inventory.objects.get(store=store)
            inventoryID = inventory.id
            hasError, inventory_list = Inventory.get_inventory(inventory.id)
    response = {
               'status': 200,
               'inventoryID': inventoryID,
               'contents': inventory_list,
               'errors': errors
              }
    return HttpResponse(json.dumps(response), content_type='application/json', status=200)

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
    picture = post.get('picture', '')
    if not picture:
        picture = default_image
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
def get_item(request):
    assert request.method == 'GET', 'api/item/get requires a GET request'
    hasError = False
    retData = { 
                "status": 200,
                "errors": []
                }

    itemID = request.GET.get('itemID', '')    
    if itemID == "":
        retData["errors"].append("itemID must be non-empty")
        hasError = True
    if not hasError:
        hasError, item = Item.get_item(itemID)
        if hasError:
            retData["errors"].append("Can't get item from itemID")
        retData["item"] = item
    return HttpResponse(json.dumps(retData), content_type='application/json', status=200)

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
        ListItem.objects.filter(item_id=itemID).delete()
        Item.objects.filter(id=itemID).delete()
    reponse = {
               'status': 200,
               'errors': errors,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

def getZip(address):
    return address.split('\n')[4]

@csrf_exempt
def create_list(request):
    assert request.method == 'POST', 'api/list/create requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    errors, user = extract_user(request, errors)
    if len(errors) > 0:
        username = ''
    else:
        username = user.username
    name = post.get('name', '')
    if not name:
        errors.append('name must be non-empty')
    if len(errors) == 0:
        try:
            new_list = CartList.create_new_list(username, name)
        except ValidationError as e:
            new_list = None
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
def get_list(request):
    hasError = False
    retData = { 
                "status": 200,
                "errors": []
                }

    listID = request.GET.get('listID', '')    
    if listID == "":
        retData["errors"].append("listID must be non-empty")
        hasError = True
    if not hasError:
        hasError, cartlist = CartList.get_cartlist(listID)
        if hasError:
            retData["errors"].append("Can't get list from listID")
        retData["list"] = cartlist
    return HttpResponse(json.dumps(retData), content_type='application/json', status=200)


@csrf_exempt
def get_user_lists(request):
    assert request.method == 'GET', 'api/list/getID requires a GET request'
    errors = []
    errors, user = extract_user(request, errors)
    if len(errors) > 0:
        listIDs = []
    else:
        listIDs = list(CartList.objects.filter(user=user).order_by('id').values_list('id', flat=True))
    all_lists = []
    for listID in listIDs:
        hasError, cartlist = CartList.get_cartlist(listID)
        if hasError:
            errors.append("Can't get list from listID")
        else:
            name = CartList.objects.get(id=listID).name
            entry = {
                     'listName': name, 
                     'listID': listID,
                     'contents': cartlist
                    }
            all_lists.append(entry)
    response = {
                'status': 200,
                'listIDs': listIDs,
                'allLists': all_lists,
                'errors': errors,
               }
    return HttpResponse(json.dumps(response), content_type='application/json', status=200)

@csrf_exempt
def get_listIDs(request):
    assert request.method == 'GET', 'api/list/getID requires a GET request'
    errors = []
    errors, user = extract_user(request, errors)
    if len(errors) > 0:
        listIDs = []
    else:
        listIDs = CartList.objects.filter(user=user).order_by('id').values_list('id', flat=True)
    response = { 
                "status": 200,
                "listIDs": listIDs,
                "errors": []
                }
    return HttpResponse(json.dumps(response), content_type='application/json', status=200)

@csrf_exempt
def delete_list_with_id(request):
    assert request.method == 'POST', 'api/list/delete requires a POST request'
    errors = []
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    listID = post.get('listID', '')
    try:
        listID = int(listID)
    except ValueError:
        listID = None
        errors.append('listID must be an integer')
    if len(errors) == 0:
        try:
            new_list = CartList.delete_list_with_id(listID)
        except ValidationError as e:
            errors.append(e)
        if not new_list:
            errors.append('no list of this listID exists')
    return return_error(errors)


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
            refill = 1
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
    entry = None
    if len(errors) == 0:
        hasError, cartlist = CartList.get_cartlist(listID)
        if hasError:
            errors.append("Can't get list from listID")
        else:
            name = CartList.objects.get(id=listID).name
            entry = {
                     'listName': name, 
                     'listID': listID,
                     'contents': cartlist
                    }
    reponse = {
               'status': 200,
               'entry': entry,
               'errors': errors,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')

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

@csrf_exempt
def add_review(request):
    assert request.method == 'POST', 'api/review/add requires a POST request'
    errors = []
    errors, user = extract_user(request, errors)
    post = QueryDict('', mutable=True)
    post.update(json.loads(request.body))
    itemID = post.get('itemID', '')
    storeID = post.get('itemID', '')
    rating = post.get('rating', '')
    text = post.get('text', '')
    item = None
    if itemID:
        try:
            itemID = int(itemID)
            if Item.objects.filter(id=itemID):
                item = Item.objects.get(id=itemID)
            else:
                item = None
                errors.append('itemID not valid')
        except ValueError:
            item = None
            errors.append('itemID must be an integer')
    if storeID:
        try:
            storeID = int(storeID)
            if Store.objects.filter(id=storeID):
                store = Store.objects.get(id=storeID)
            else:
                store = None
                errors.append('storeID not valid')
        except ValueError:
            store = None
            errors.append('storeID must be an integer')
    elif item:
        store = item.store
    else:
        errors.append('must provide valid storeID or itemID')
    try:
        rating = int(rating)
    except ValueError:
        errors.append('rating must be an integer')
    else:
        if (rating < 1) or (rating > 5):
            errors.append('rating must be an integer between 1 and 5, inclusively')
    if len(errors) == 0:
        try:
            new_review = Review.create_new_review(user, item, store, rating, text)
        except ValidationError as e:
            new_review = None
            errors.append(e)
    return return_error(errors)


@csrf_exempt
def get_reviews(request):
    assert request.method == 'GET', 'api/review/get requires a GET request'
    errors = []
    storeID = request.GET.get('storeID', '')
    itemID = request.GET.get('itemID', '')
    reviewID = request.GET.get('reviewID', '')
    review_list = []
    if itemID:
        try:
            itemID = int(itemID)
            if Item.objects.filter(id=itemID):
                item = Item.objects.get(id=itemID)
            else:
                item = None
                errors.append('itemID not valid')
        except ValueError:
            item = None
            errors.append('itemID must be an integer')
        if item:
            review_list = Review.get_item_reviews(item)
    elif storeID:
        try:
            storeID = int(storeID)
            if Store.objects.filter(id=storeID):
                store = Store.objects.get(id=storeID)
            else:
                store = None
                errors.append('storeID not valid')
        except ValueError:
            store = None
            errors.append('storeID must be an integer')
        if store:
            review_list = Review.get_store_reviews(store)
    elif reviewID:
        try:
            reviewID = int(reviewID)
        except ValueError:
            errors.append('reviewID must be an integer')
        status, current_review = Review.get_review(reviewID)
        if status:
            errors.append('reviewID invalid')
        else:
            review_list = [current_review]
    else:
        errors.append('must provide valid storeID or itemID')
    reponse = {
               'status': 200,
               'reviews': review_list,
               'errors': errors,
              }
    return HttpResponse(json.dumps(reponse), content_type='application/json')



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
    if not location.strip():
        errors.append('location must be non-empty')
        location_coord = (0, 0)
    else:
        location_coord = lat_lon(location)
        if not location_coord:
            location_coord = (0, 0)
    json_items = []
    if len(errors) == 0:
        items, search_errors = Item.search_items(query, location)
        if len(errors) > 0:
            errors += search_errors
        elif len(items) == 0:
            errors.append('query returned no results')
        else:
            i = 0
            for current_item in items:
                i += 1
                store = current_item.store
                item = {
                        'itemID': current_item.id,
                        'storeID': store.id,
                        'storeName': store.name,
                        'name': current_item.name,
                        'description': current_item.description,
                        'picture': current_item.picture,
                        'price': current_item.price,
                        'address_street': store.address_street,
                        'address_city': store.address_city,
                        'address_state': store.address_state,
                        'address_zip': store.address_zip,
                        'index': i,
                        }
                address_list = [
                                item['address_street'],
                                item['address_city'],
                                item['address_state'],
                                item['address_zip'],
                               ]
                address = ' '.join(address_list)
                # Google geo-caching is limited to 10 per second without a paid API key
                if ((i + 1) % 10) == 0:
                    time.sleep(1)
                coord = lat_lon(address)
                if coord:
                    item['latitude'] = coord[0]
                    item['longitude'] = coord[1]
                    item['coordinates'] = 1
                else:
                    item['latitude'] = 0
                    item['longitude'] = 0
                    item['coordinates'] = 0

                json_items.append(item)
    response = {
               'status': 200,
               'items': json_items,
               'latitude': location_coord[0],
               'longitude': location_coord[1],
               'errors': errors
              }
    return HttpResponse(json.dumps(response), content_type='application/json')


def extract_user(request, errors):
    user = None
    if request.method == 'POST':
        if request.body:
            post = QueryDict('', mutable=True)
            post.update(json.loads(request.body))
            username = post.get('username', '')
        else:
            username = ''
    else:
        get = request.GET
        username = get.get('username', '')
    if username:
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            user = None
            errors.append('username does not exist')
    else:
        user = request.user
        if not user.is_authenticated():
            errors.append('user not logged in')
    return errors, user


def import_inventory(request):
    assert request.method == 'POST', 'api/inventory/import requires a POST request'
    errors = []
    # try:
    post = request.POST
    files = request.FILES
    inventoryID = post.get('inventoryID', '')
    imported_file = files['dataset']
    path = default_storage.save('temporary.csv', ContentFile(imported_file.read()))
    dataset = tablib.Dataset()
    dataset.csv = default_storage.open(path).read()
    try:
        dataset.headers = ('id', 'name', 'description', 'price', 'picture')
    # except Exception as e:
    #     errors.append('%s (%s)' % (e.message, type(e))) 
    #     errors.append('File formatted incorrectly: check for dollar signs in prices or missing columns')
    except tablib.core.InvalidDimensions:
        errors.append('File formatted incorrectly: missing columns')
    try:
        inventoryID = int(inventoryID)
    except ValueError:
        inventoryID = None
        errors.append('inventoryID must be integers')
    items = []
    if len(errors) == 0:
        if not Inventory.objects.filter(id=inventoryID).exists():
            errors.append('inventoryID is not valid')
            map_markers = []
        else:
            storeID = Inventory.objects.get(id=inventoryID).store.id
            store_list = []
            inventory_list = []
            for x in xrange(dataset.height):
                store_list.append(storeID)
                inventory_list.append(inventoryID)
            dataset.append_col(col=store_list, header='store')
            dataset.append_col(col=inventory_list, header='inventory')
            item_resource = ItemResource()
            result = item_resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                    result = item_resource.import_data(dataset, dry_run=False)
            else:
                errors.append('not correct')
            queryset = Item.objects.filter(inventory=inventoryID)
            counter = 0
            for i in queryset:
                counter += 1
                items.append({
                              'itemID' : i.id,
                              'storeName': i.store.name,
                              'index': counter,
                              'name': i.name,
                              'description': i.description,
                              'price': i.price,
                              })
    reponse = {
               'status': 200,
               'items': items,
               'errors': errors,
              }
    default_storage.delete(path)
    # except ValueError:
    #     errors.append('%s (%s)' % (e.message, type(e))) 
    #     errors.append('File formatted incorrectly: check for dollar signs in prices or missing columns')
    return HttpResponse(json.dumps(reponse), content_type='application/json')




