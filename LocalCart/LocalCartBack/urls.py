from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^api/user/create$', views.create_user),
    url(r'^api/user/login$', views.log_in),
    url(r'^api/store/create$', views.create_store),
    url(r'^api/inventory/create$', views.create_inventory),
    url(r'^api/inventory/add$', views.create_item),
    url(r'^api/item/create$', views.create_item),
    url(r'^api/item/edit$', views.edit_item),
]


