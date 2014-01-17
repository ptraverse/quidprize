from django import forms
from apps.qp.models import Business

class BusinessForm(forms.ModelForm):
	class Meta:
		model = Business
		fields = ['auth_user','name','contact_person','contact_phone']

