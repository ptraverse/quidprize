import bitly_api
import socket
import sys
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.http import *
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from apps.qp.forms import BusinessForm

def index(request):
	return render(request, 'index.html' )

def business(request):
	if request.method == 'POST': # If the form has been submitted...
        	form = BusinessForm(request.POST) # A form bound to the POST data
        	if form.is_valid(): # All validation rules pass
        		# Process the data in form.cleaned_data
        		# ...
        		return HttpResponseRedirect('/thanks/') # Redirect after POST
    	else:
        	form = BusinessForm() # An unbound form

	return render(request, 'business.html', { 'form': form, } )		
