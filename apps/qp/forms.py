from django import forms
from apps.qp.models import *
from django.core.validators import *

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
    class Meta:
        model = Raffle
        fields = ['target_url','expiry_date']

class BetaRaffleForm(forms.ModelForm):
    contact_name = forms.CharField()
    contact_phone = forms.CharField()
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
    def clean(self):
        username = self.cleaned_data.get('username')
        username_confirm = self.cleaned_data.get('username_confirm')
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        validate_email(username)
        if username and username != username_confirm:
            raise forms.ValidationError("Emails don't match")
        if password and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data
        
