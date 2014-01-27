from django import forms
from apps.qp.models import Business, User

class BusinessForm(forms.ModelForm):
	class Meta:
		model = Business
		fields = ['auth_user','name','contact_person','contact_phone']

class UserForm(forms.ModelForm):
    username_confirm = forms.CharField()
    password_confirm = forms.CharField()
    class Meta:
        model = User
        fields = ['username','password']
        
        

