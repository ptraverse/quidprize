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

from apps.qp.forms import BusinessForm, UserForm


def business(request):
    if request.method == 'POST': # If the form has been submitted...
        form = BusinessForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = BusinessForm() # An unbound form
    return render(request, 'business.html', {'form': form, })

def log_in(request):
    if request.method == 'POST':
        login_email = request.POST.get("log_in_email","")
        login_password = request.POST.get("log_in_password","")
        username = User.objects.get(email=login_email)
        user = authenticate(username=username, password=login_password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../')
            else:
                return HttpResponseRedirect('../reset-password')
        else:
            return HttpResponseRedirect('../register')
    else:
        print("request not POST!!")
        return render(request, '500.html' )

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        bf = BusinessForm(request.POST, prefix='business')
        if uf.is_valid() * bf.is_valid():
            user = uf.save()
            business = bf.save(commit=False)
            business.user = user
            business.save()            
        return HttpResponseRedirect('/')
    else:
        uf = UserForm()
        bf = BusinessForm()
        return render(request, 'register.html', {'userform':uf , 'businessform':bf } )

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return render(request, 'user_home.html', {'request_user':request.user } )

