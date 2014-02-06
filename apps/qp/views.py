import socket
import sys
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.hashers import *
from django.contrib.auth.models import *
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import *
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.utils import simplejson

from apps.qp.forms import *
import owly_api

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

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return render(request, 'user_home.html', {'request_user':request.user } )

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect('/')
    else:
        form = DocumentForm() # A empty, unbound form
    # Load documents for the list page
    documents = Document.objects.all()
    # Render list page with the documents and the form
    return render(request, 'list.html',{'documents': documents, 'form': form} )

def log_in(request):
    if request.method == 'POST':
        login_email = request.POST.get("log_in_email","")
        login_password = request.POST.get("log_in_password","")
        try:
            username = User.objects.get(email=login_email)
        except User.DoesNotExist:
            return HttpResponseRedirect('../register')
        user = authenticate(username=username, password=login_password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../')
            else:
                return HttpResponseRedirect('../reset-password')
        elif username is not None: #username exists but password is incorrect
            return HttpResponseRedirect('/')

    else: #should never get here
        return render(request, '500.html' )

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def raffle(request):
    if request.method == 'POST':
        try:
            business = Business.objects.get(auth_user=request.user)
        except Business.DoesNotExist:
            return render(request, '500.html' , {'message':'No business corresponding to request user'})
        except TypeError: #user timed out
            return HttpResponseRedirect('/')
        rf = RaffleForm(request.POST)
        if rf.is_valid():
            raffle = rf.save(commit=False)
            raffle.business = business
            raffle.date_created = datetime.now()
            raffle.save()
            return HttpResponseRedirect('/')
        else:
            print(rf.errors)
            return HttpResponseRedirect('../raffle/')
    else:
        rf = RaffleForm()
        return render(request, 'raffle.html', {'raffleform':rf} )

def raffles(request):
    rafflelist = Raffle.objects.all()
    return render(request, 'raffles.html', {'rafflelist':rafflelist} )

def raffle_email(request, raffle_id, activation_email):
    t = Ticket.objects.filter(raffle=raffle_id).filter(activation_email=activation_email) #probably ways to optimise this
    return HttpResponseRedirect('../')

def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        bf = BusinessForm(request.POST)
        if uf.is_valid() * bf.is_valid():
            user = uf.save(commit=False)
            import random
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, uf.cleaned_data['password'])
            user.password = '%s$%s$%s' % (algo, salt, hsh)
            user.email = user.username
            user.save()
            business = bf.save(commit=False)
            business.user = user
            business.save()
        elif uf.is_valid():
            user = uf.save(commit=False)
            import random
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, uf.cleaned_data['password'])
            user.password = '%s$%s$%s' % (algo, salt, hsh)
            user.email = user.username
            user.save()
        else:
            print(uf.errors)
            print(bf.errors)
        return HttpResponseRedirect('/')
    else:
        uf = UserForm()
        bf = BusinessForm()
        return render(request, 'register.html', {'userform':uf , 'businessform':bf } )

def ticket(request):
    if request.method == 'POST':
        tf = TicketForm(request.POST)
        if tf.is_valid():
            ticket = tf.save(commit=False)
            ticket.date_activated = datetime.now()
            Owly = owly_api.Owly()
            response = Owly.url_shorten(ticket.raffle.target_url)
            print response
            ticket.owly_hash = response['results']['hash']
            ticket.save()
            return HttpResponseRedirect('/')
        else:
            print(tf.errors)
            return HttpResponseRedirect('../ticket/')
    else:
        tf = TicketForm()
        return render(request, 'ticket.html', {'ticketform':tf} )

def tickets(request):
    tl = Ticket.objects.all()
    return render(request, 'tickets.html', {'ticketlist':tl} )

def ticket_activation(request, raffle_id):
    if request.method == 'POST':
        taf = TicketActivationForm(request.POST)
        if taf.is_valid():
            ticket = taf.save(commit=False)
            ticket.save()
            return HttpResponseRedirect('/')
        else:
            print(taf.errors)
            return HttpResponseRedirect('../'+raffle_id)
    else:
        taf = TicketActivationForm()
        r = Raffle.objects.get(id=raffle_id)
        return render(request, 'ticket_activation.html', {'ticketactivationform':taf, 'raffle':r} )

def ticket_activation_json(request,raffle_id):
    if request.POST.has_key('client_response'):
        print(request.POST)
        ticket = Ticket.objects.create(raffle_id=raffle_id,date_activated = datetime.now())
        ticket.activation_email = request.POST.get('client_response')
        try:
            user = User.objects.get(email=ticket.activation_email)
        except User.DoesNotExist:
            user = User.objects.create(username=ticket.activation_email,email=ticket.activation_email)
        Owly = owly_api.Owly()
        tid_url = request.get_host()
        tid_url = tid_url + '/tid/'
        tid_url = tid_url + str(ticket.id)
        print(tid_url)
        response = Owly.url_shorten(tid_url)
        ticket.owly_hash = response['results']['hash']
        ticket.save()
        response_dict = {}
        response_dict.update({'owly_hash': ticket.owly_hash  })
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    else:
        print(request.POST)
        return render(request, '500.html', {'message':'request post missing key "client response"'})

def ticket_id(request, ticket_id):
    t = Ticket.objects.get(id=ticket_id)
    if request.user.is_authenticated():
        return render(request, 'ticket_stats.html', {'ticket':t} )
    else:
        return HttpResponseRedirect(t.raffle.target_url)
