from django import forms
from apps.qp.models import *

class BusinessForm(forms.ModelForm):
	class Meta:
		model = Business
		fields = ['auth_user','name','logo','contact_person','contact_phone']

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

class RaffleForm(forms.ModelForm):
    legal_agreement = forms.BooleanField()
    class Meta:
        model = Raffle
        fields = ['target_url','expiry_date']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['activation_email','raffle']

class TicketActivationForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['activation_email']

class UserForm(forms.ModelForm):
    username_confirm = forms.CharField()
    password_confirm = forms.CharField()
    class Meta:
        model = User
        fields = ['username','password']
        
