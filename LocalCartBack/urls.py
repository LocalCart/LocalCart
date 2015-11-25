from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^api/user/create$', views.create_user),
    url(r'^api/user/edit$', views.edit_user),
    url(r'^api/user/destroy$', views.empty_db),
    url(r'^api/user/login$', views.log_in),
    url(r'^api/user/logout$', views.log_out),
    url(r'^api/user/get$', views.return_user),
    url(r'^api/store/create$', views.create_store),
    url(r'^api/store/edit$', views.edit_store),
    url(r'^api/store/getUser$', views.get_store_user),
    url(r'^api/store/storeID$', views.get_store),
    url(r'^api/inventory/create$', views.create_inventory),
    url(r'^api/inventory/store$', views.get_inventory_store),
    # url(r'^api/inventory/create$', views.create_inventory),
    url(r'^api/inventory/add$', views.create_item),
    url(r'^api/inventory/getUser$', views.get_user_inventory),
    url(r'^api/inventory/import$', views.import_inventory),
    url(r'^api/item/create$', views.create_item),
    url(r'^api/item/edit$', views.edit_item),
    url(r'^api/item/delete$', views.delete_item),
    url(r'^api/list/create$', views.create_list),
    url(r'^api/list/delete$', views.delete_list),
    url(r'^api/list/deleteid$', views.delete_list_with_id),
    url(r'^api/list/edit$', views.edit_list),
    url(r'^api/list/map$', views.map_list),
    url(r'^api/list/get$', views.get_list),
    url(r'^api/list/getID$', views.get_listIDs),
    url(r'^api/list/getUser', views.get_user_lists),
    url(r'^api/search/items$', views.search_items),
    url(r'^merchant$', views.merchant_render),
    url(r'^home$', views.home),
    url(r'^register$', views.register_render),
    url(r'^login$', views.login_render),
    url(r'^search$', views.search_render),
    url(r'^inventory$', views.inventory_render),
    url(r'^store$', views.store_render),
]