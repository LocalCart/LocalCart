from django.shortcuts import render
from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from models import *
import time
from forms import *
from django.contrib.auth import authenticate, login, logout
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
    post = request.POST
    files = request.FILES
    form = NewUserForm(post, files)
    if form.is_valid():
        username = post.get('username', '')
        password = post.get('password', '')
        user_type = post.get('user_type', '')
        email = post.get('email', '')
        picture = files['picture']
        first_name = post.get('first_name', '') # Optional
        last_name = post.get('last_name', '') # Optional

        new_user_info = UserInfo.create_new_user(username, password, email, first_name, last_name, user_type, picture)
        if new_user_info:
            return HttpResponseRedirect('home') # TODO: redirect to "successfully registered" page??? re-render page???
        else:
            form.errors['username'] = [u'Username already exists.']
    response = {
               'status': 200,
               'errors': form.errors,
              }
    return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def edit_user(request):
    assert request.method == 'POST', 'api/user/change requires a POST request'
    post = request.POST
    files = request.FILES
    form = EditUserForm(post, files)
    if form.is_valid():
        username = post.get('username', '')
        password = post.get('password', '')
        email = post.get('email', '')
        if files:
            picture = files['picture']
        else:
            picture = ''
        first_name = post.get('first_name', '') # Optional
        last_name = post.get('last_name', '') # Optional

        current_user_info = UserInfo.edit_user_info(username=username, first_name=first_name, last_name=last_name, email=email, password=password, picture=picture)
        if current_user_info:
            return HttpResponseRedirect('home') # TODO: redirect to "user profile" page??? re-render page???
        else:
            form.errors['username'] = [u'Username does not exist.']
    response = {
               'status': 200,
               'errors': form.errors,
              }
    return HttpResponse(json.dumps(response), content_type='application/json')

    
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
    post = request.POST
    files = request.FILES
    form = NewStoreForm(post, files)
    if form.is_valid():
        username = post.get('username', '')
        name = post.get('name', '')
        description = post.get('description', '')
        picture = files['picture']
        address_street = post.get('address_street', '')
        address_apt = post.get('address_apt', '')
        address_city = post.get('address_city', '')
        address_state = post.get('address_state', '')
        address_zip = post.get('address_zip', '')
        phone_number = post.get('phone_number', '')

        new_store = Store.create_new_store(username=username, name=name, description=description, picture=picture,
                          address_street=address_street, address_apt=address_apt, address_city=address_city, address_state=address_state, address_zip=address_zip, phone_number=phone_number)
        if new_store:
            if new_store == 'exists':
                form.errors['address'] = [u'Another store already exists at this address.']
            else:
                return HttpResponseRedirect('home') # TODO: redirect to "user profile" page??? re-render page???
        else:
            form.errors['username'] = [u'Username does not exist.']
    response = {
               'status': 200,
               'errors': form.errors,
              }
    return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def edit_store(request):
    assert request.method == 'POST', 'api/store/edit requires a POST request'
    post = request.POST
    files = request.FILES
    form = EditStoreForm(post, files)
    if form.is_valid():
        storeID = post.get('storeID', '')
        name = post.get('name', '')
        description = post.get('description', '')
        if files:
            picture = files['picture']
        address_street = post.get('address_street', '')
        address_apt = post.get('address_apt', '')
        address_city = post.get('address_city', '')
        address_state = post.get('address_state', '')
        address_zip = post.get('address_zip', '')
        phone_number = post.get('phone_number', '')

        edited_store = Store.edit_store(storeID=storeID, name=name, description=description, picture=picture,
                          address_street=address_street, address_apt=address_apt, address_city=address_city, address_state=address_state, address_zip=address_zip, phone_number=phone_number)
        if edited_store:
            if edited_store == 'exists':
                form.errors['address'] = [u'Another store already exists at this address.']
            else:
                return HttpResponseRedirect('home') # TODO: redirect to "user profile" page??? re-render page???
        else:
            form.errors['store'] = [u'Store does not exist.']
    response = {
               'status': 200,
               'errors': form.errors,
              }
    return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
def get_store(request):
    hasError = False
    retData = { 
                "status": 200,
                "errors": []
                }

    store_id = request.GET.get('store_id', '')    
    if store_id == "":
        retData["errors"].append("store_id must be non-empty")
        hasError = True
    if not hasError:
        hasError, store = Store.get_store(store_id)
        if hasError:
            retData["errors"].append("Can't get store from store_id")
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

    inventory_id = request.GET.get('inventory_id', '')    
    if inventory_id == "":
        retData["errors"].append("inventory_id must be non-empty")
        hasError = True
    if not hasError:
        hasError, inventory = Inventory.get_inventory(inventory_id)
        if hasError:
            retData["errors"].append("Can't get inventory from inventory_id")
        retData["inventory"] = inventory
    return HttpResponse(json.dumps(retData), content_type='application/json', status=200)

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
def get_item(request):
    hasError = False
    retData = { 
                "status": 200,
                "errors": []
                }

    item_id = request.GET.get('item_id', '')    
    if item_id == "":
        retData["errors"].append("item_id must be non-empty")
        hasError = True
    if not hasError:
        hasError, item = Item.get_item(item_id)
        if hasError:
            retData["errors"].append("Can't get inventory from inventory_id")
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
def get_list(request):
    hasError = False
    retData = { 
                "status": 200,
                "errors": []
                }

    list_id = request.GET.get('list_id', '')    
    if list_id == "":
        retData["errors"].append("list_id must be non-empty")
        hasError = True
    if not hasError:
        hasError, cartlist = Inventory.get_list(list_id)
        if hasError:
            retData["errors"].append("Can't get list from list_id")
        retData["list"] = cartlist
    return HttpResponse(json.dumps(retData), content_type='application/json', status=200)


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
