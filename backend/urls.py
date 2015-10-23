from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'backend.views.home'),
    url(r'^api/user/create$', 'backend.views.create_user'),
    url(r'^api/user/login$', 'backend.views.log_in'),
    url(r'^api/store/create$', 'backend.views.create_store'),
    url(r'^api/inventory/create$', 'backend.views.create_inventory'),
    url(r'^api/inventory/add$', 'backend.views.create_item'),
    url(r'^api/item/create$', 'backend.views.create_item'),
    url(r'^api/item/edit$', 'backend.views.edit_item'),
    url(r'^api/search/items$', 'backend.views.search_items'),
]


