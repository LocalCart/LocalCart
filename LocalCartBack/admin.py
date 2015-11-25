from django.contrib import admin
from import_export import resources
from models import *

# Register your models here.
class ItemResource(resources.ModelResource):
	class Meta:
		model = Item
		skip_unchanged = True
		report_skipped = True
		# exclude = ('store', 'inventory')