import models
from django import forms

class NewUserForm(forms.ModelForm):
	class Meta:
		model = models.UserInfo
		fields = ['user_type', 'picture']
	username = forms.CharField(label="Username")
	password = forms.CharField(label="Password")
	email = forms.EmailField(label="Email")
	first_name = forms.CharField(label="First Name", required=False)
	last_name = forms.CharField(label="Last Name", required=False)

class EditUserForm(forms.Form):
	username = forms.CharField(label="Username")
	password = forms.CharField(label="Password", required=False)
	email = forms.EmailField(label="Email", required=False)
	picture = forms.ImageField(label="Profile Picture", required=False)
	first_name = forms.CharField(label="First Name", required=False)
	last_name = forms.CharField(label="Last Name", required=False)

class NewStoreForm(forms.ModelForm):
	class Meta:
		model = models.Store
		fields = ['name', 'description', 'picture', 'address_street', 'address_apt', 'address_city', 'address_state', 'address_zip', 'phone_number']
	username = forms.CharField(label="Username")

class EditStoreForm(forms.ModelForm):
	class Meta:
		model = models.Store
		fields = ['name', 'description', 'picture', 'address_street', 'address_apt', 'address_city', 'address_state', 'address_zip', 'phone_number']
	storeID = forms.IntegerField(label="Store ID")
	def __init__(self, *args, **kwargs):
		super(EditStoreForm, self).__init__(*args, **kwargs)
		self.fields['name'].required = False
		self.fields['description'].required = False
		self.fields['picture'].required = False
		self.fields['address_street'].required = False
		self.fields['address_apt'].required = False
		self.fields['address_city'].required = False
		self.fields['address_state'].required = False
		self.fields['address_zip'].required = False
		self.fields['phone_number'].required = False



















