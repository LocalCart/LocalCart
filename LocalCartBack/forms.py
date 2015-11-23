import models
from django import forms
from django.core.validators import RegexValidator

# class AddressField(MultiValueField):
#     def __init__(self, *args, **kwargs):
#         # Define one message for all fields.
#         error_messages = {
#             'incomplete': 'Enter an address.',
#         }
#         # Or define a different message for each field.
#         fields = (
#             forms.CharField(error_messages={'incomplete': 'Enter a country calling code.'},
#                       validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code.')]),
#             forms.CharField(error_messages={'incomplete': 'Enter a phone number.'},
#                       validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')]),
#             forms.CharField(validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid extension.')],
#                       required=False),
#         )
#         super(AddressField, self).__init__(
#             error_messages=error_messages, fields=fields,
#             require_all_fields=False, *args, **kwargs)

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
	username = forms.CharField(label="Username")
	name = forms.CharField(label="Store Name")
	description = forms.CharField(label="Store Description")
	picture = forms.ImageField(label="Store Picture")
	address_street = forms.CharField(label="Address Street")
	address_city = forms.CharField(label="City")
	address_state = forms.CharField(label="State")
	address_zip = forms.CharField(label="Zip Code", min_length=5, max_length=5)
	phone_number = forms.CharField(label="Phone Number", min_length=10)