from django import forms

class NewUserForm(forms.Form):
	username = forms.CharField(label="Username")
	password = forms.CharField(label="Password")
	CUSTOMER = 'CR'
	MERCHANT = 'MT'
	USER_TYPE_CHOICES = (
		(CUSTOMER, 'Customer'),
		(MERCHANT, 'Merchant'),
	)
	user_type = forms.ChoiceField(label="User Type", choices=USER_TYPE_CHOICES)
	email = forms.EmailField(label="Email")
	picture = forms.ImageField(label="Profile Picture")
	first_name = forms.CharField(label="First Name", required=False)
	last_name = forms.CharField(label="Last Name", required=False)