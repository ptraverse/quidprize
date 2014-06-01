from django import forms
from apps.qp.models import *
from django.core.validators import *
import re

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
    class Meta:
        model = Raffle
        fields = ['target_url','logo_upload','expiry_date']
    def clean(self):
        target_url = self.cleaned_data.get('password')
        url_validate = URLValidator()
        url_validate(target_url)
        expiry_date = self.cleaned_data.get('password_confirm')
        return self.cleaned_data
class BetaRaffleForm2(forms.ModelForm):
    class Meta:
        model = Prize
        fields = ['description','value']
class BetaRaffleForm3(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['masked_credit_card_number','credit_card_type','payment_date','payment_result','payment_type']

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
        
