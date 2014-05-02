import socket
import sys
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

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
from apps.qp.models import *
import owly_api
import bitly_api
from gexf import Gexf, GexfImport
from lxml import etree

@login_required
def beta_new_raffle(request):
    if request.method == 'POST': # If the form has been submitted...
        brf = BetaRaffleForm(request.POST) # A form bound to the POST data
        if brf.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #use logger
            r = brf.save(commit=False)
            r.business_id='-1'
            msg = "New Raffle Request. Phone Immediately : "
            msg = msg + request.POST.get('contact_name') + ' @ '
            msg = msg + request.POST.get('contact_phone') + ' | '
            msg = msg + request.POST.get('target_url') + ' | '
            msg = msg + request.POST.get('expiry_date') + ' | '
            msg = msg + request.user.email
            logger.info(msg)
            print(brf)
            return HttpResponseRedirect('/thanks/') # Redirect after POST
        else:
            print brf.errors
            return render(request,'beta_raffle.html',{'betaraffleform':brf})
    else:
        brf = BetaRaffleForm()
        return render(request,'beta_raffle.html',{'betaraffleform':brf})


def business_create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = BusinessForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = BusinessForm() # An unbound form
    return render(request, 'business.html', {'form': form, })

def business(request,business_name):
    try:
        b = Business.objects.get(name=business_name)
    except Business.DoesNotExist:
        return render(request, '500.html', {'message':'Dis Bizness '+business_name+' DNE'})
    rl = Raffle.objects.filter(business=b.id)
    r = rl[0]
    taf = TicketActivationForm()
    return render(request, 'b.html', {'business': b, 'raffle':r, 'ticketactivationform':taf})

def completion_logger(request):
    tid = request.GET.get('ticket_id')
    hr = request.META.get('HTTP_REFERER')
    ra = request.META.get('REMOTE_ADDR')
    ruid = request.GET.get('user_id')
    c = Completion.objects.create(ticket=Ticket.objects.get(id=tid))
    c.http_referer = hr
    c.remote_addr = ra
    if str(ruid) > '0':
        c.remote_user = User.objects.get(id=ruid)
    c.save()
    response_dict = {}
    response_dict.update({'success': True })
    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

def index(request):
    if not request.user.is_authenticated():
        logger.info('Index '+request.META['REMOTE_ADDR']+' - '+request.META['HTTP_USER_AGENT'])
        return render(request, 'index.html')
    else:
        return render(request, 'user_home.html', {'request_user':request.user } )

def legal(request):
    return render(request, 'legal.html');

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
            return HttpResponseRedirect('../register/')
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
        return HttpResponseRedirect('/beta_new_raffle/')
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
    for r in rafflelist:
        r.root_ticket = r.get_root_ticket()
    rf = RaffleForm()
    return render(request, 'raffles.html', {'rafflelist':rafflelist, 'raffleform':rf} )

def raffle_countdown_test(request):
    return render(request, 'raffle_countdown_test.html' );

def raffle_email(request, raffle_id, activation_email):
    t = Ticket.objects.filter(raffle=raffle_id).filter(activation_email=activation_email) #probably ways to optimise this
    return HttpResponseRedirect('../')

def raffle_div_test(request,raffle_id):
    r = Raffle.objects.get(id=raffle_id)
    return render(request, 'raffle_div.html', {'raffle':r} )

def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        bf = BusinessForm(request.POST)
        if (uf.is_valid() and bf.is_valid()):
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
            logmsg = "New Business "+business.name+" Created: "+business.contact_person+" "+business.contact_person
            logger.info(logmsg) #log for immediate response in R.L.
            print logmsg
            userauth = authenticate(username=user, password=uf.cleaned_data['password'])
        elif uf.is_valid():
            user = uf.save(commit=False)
            import random
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, uf.cleaned_data['password'])
            user.password = '%s$%s$%s' % (algo, salt, hsh)
            user.email = user.username
            user.save()
            logmsg = "New User "+user.username+" Created"
            logger.info(logmsg) #log for immediate response in R.L.
            userauth = authenticate(username=user, password=uf.cleaned_data['password'])
            login(request, userauth)
        else:
            print(uf.errors)
            print('---')
            print(bf.errors)
            return render(request, 'register.html', {'userform':uf , 'businessform':bf } )
        return HttpResponseRedirect('/')
    else:
        uf = UserForm()
        bf = BusinessForm()
        return render(request, 'register.html', {'userform':uf , 'businessform':bf } )

def sigma_test(request):
    g = {}
    return render(request, 'sigma_test.html', {'json':g})

def sigma_test_json(request):
    r = Raffle.objects.get(id='58')
    tl = Ticket.objects.filter(raffle=r.id)
    print tl
    nodes = []
    edges = []
    for t in tl:
        n = {}
        n.update({'id':'n'+str(t.id),'label':t.hash,'x':0,'y':2,'size':1})
        nodes.append(n)
        if t.parent_ticket_id>0:
            e = {}
            e.update({'id':t.id,'source':t.id,'target':t.parent_ticket_id})
            edges.append(e)
    g = {}
    g.update({'nodes':nodes,'edges':edges})
    return HttpResponse(simplejson.dumps(g), content_type="application/json")
    #return render(request, 'sigma_test.html', {'json':simplejson.dumps(g),'content_type':"application/json"})
    # return render(request, 'sigma_test.html', {'json':g})

def sigma_gexf(request, ticket_hash):
    x = Ticket.objects.get(hash=ticket_hash)
    r = Raffle.objects.get(id=x.raffle.id)
    tl = Ticket.objects.filter(raffle=r.id).order_by('-is_root_ticket')
    gexf = Gexf('Tree For '+ticket_hash,'Sigma JS Graph')
    graph = gexf.addGraph('directed','static',ticket_hash)
    graph.addNodeAttribute('xcoord','0',"float")
    graph.addNodeAttribute('ycoord','0',"float")
    graph.addNodeAttribute('label','',"string")
    graph.addNodeAttribute('completion_size','1',"float")
    coords = r.graph()
    for i,t in enumerate(tl):
        n = graph.addNode(t.id,t.hash)
        n.addAttribute(0,str(coords[i][0]))
        n.addAttribute(1,str(coords[i][1]*4))
        n.addAttribute(2,t.hash)
        cs = t.completion_count()
        n.addAttribute(3,str(cs))
    for t in tl:
        if t.parent_ticket_id>0:
            graph.addEdge(t.id,t.id,t.parent_ticket_id)
    response = etree.tostring(gexf.getXML(),pretty_print=True,encoding='utf-8',xml_declaration=True)
    return HttpResponse(response, content_type="application/json")

def sigma_test_gexf(request):
    r = Raffle.objects.get(id='58')
    tl = Ticket.objects.filter(raffle=r.id).order_by('-is_root_ticket')
    gexf = Gexf('Sample','Testting Sigma JS')
    graph = gexf.addGraph('directed','static','a test graph')
    graph.addNodeAttribute('xcoord','0',"float")
    graph.addNodeAttribute('ycoord','0',"float")
    graph.addNodeAttribute('label','',"string")
    coords = r.graph()
    for i,t in enumerate(tl):
        n = graph.addNode(t.id,t.hash)
        n.addAttribute(0,str(coords[i][0]))
        n.addAttribute(1,str(coords[i][1]))
        n.addAttribute(2,t.hash)
        if t.parent_ticket_id>0:
            graph.addEdge(t.id,t.id,t.parent_ticket_id)
    response = etree.tostring(gexf.getXML(),pretty_print=True,encoding='utf-8',xml_declaration=True)
    print response
    return HttpResponse(response, content_type="application/json")

def test_countdown(request):
    return render(request, 'countdown_test.html' )

def thanks(request):
    return render(request, 'thanks.html')

def ticket_create(request):
    if request.method == 'POST':
        tf = TicketForm(request.POST)
        if tf.is_valid():
            ticket = tf.save(commit=False)
            ticket.date_activated = datetime.now()
            API_USER = "cfd992841301aabcd843e8ed4622b9c88e320e8e"
            API_KEY = "c5955c440b750b215924bd08d1b79518ca4a82c4"
            ACCESS_TOKEN = "1214d30c74adf88608b83bdc8eac7b053a57b6f4"
            Bitly = bitly_api.Connection(access_token=ACCESS_TOKEN)
            response = Bitly.url_shorten(ticket.raffle.target_url)
            print response
            ticket.hash = response['results']['hash']
            ticket.save()
            return HttpResponseRedirect('/')
        else:
            print(tf.errors)
            return HttpResponseRedirect('../ticket/')
    else:
        tf = TicketForm()
        return render(request, 'ticket.html', {'ticketform':tf} )

def ticket(request, ticket_id):
    t = Ticket.objects.get(id=ticket_id)
    t.num_clicks = t.get_num_clicks()
    r = t.raffle
    if request.user.is_active:
        if t.activation_email == request.user.email: #if this user owns this ticket
            return render(request, 'yours.html', {'ticket':t, 'raffle':r, })
        else:
            try: #try and get this users ticket for this raffle
                t2 = Ticket.objects.get(activation_email=request.user.email, raffle=r)
                return render(request, 'not_yours.html', {'ticket':t, 'owned_ticket':t2, 'raffle':r, })
            except Ticket.DoesNotExist: # user does not own one in this raffle, show this ticket
                taf = TicketActivationForm(initial={'activation_email':request.user.email})
                return render(request, 't.html', {'ticket':t, 'raffle':r, 'ticketactivationform':taf})
    else: # not logged in
        taf = TicketActivationForm()
        return render(request, 't.html', {'ticket':t, 'raffle':r, 'ticketactivationform':taf})

def ticket_by_hash(request, hash):
    try:
        t = Ticket.objects.get(hash=hash)
    except Ticket.DoesNotExist:
        return render(request, '404.html')
    return ticket(request, t.id)

def ticket_redirect(request, ticket_id):
    try:
        t = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return render(request, '404.html')
    return HttpResponseRedirect('/'+t.hash)

def tickets(request):
    m = 'No Tickets yet'
    if request.user.is_active:
        try:
            tl = Ticket.objects.filter(activation_email=request.user.email)
            print tl
        except Ticket.DoesNotExist:
            m = m + 'You need to get some tickets activated to participate in quidprize'
        for ticket in tl:
            ticket.num_clicks = ticket.get_num_clicks()
    else:
        return render(request, '500.html', {'message':'you need to login to use this page'})
    return render(request, 'you.html', {'ticketlist':tl, 'message':m} )

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
        try:
            ticket = Ticket.objects.get(raffle=raffle_id,activation_email=request.POST.get('client_response'))
            url = 'http://ow.ly/'+ticket.hash
            status = 'existing'
            print "ticket activattion email already has ticket"
        except Ticket.DoesNotExist:
            ticket = Ticket.objects.create(raffle_id=raffle_id,date_activated = datetime.now())
            ticket.activation_email = request.POST.get('client_response')
            try:
                user = User.objects.get(email=ticket.activation_email)
            except User.DoesNotExist:
                user = User.objects.create(username=ticket.activation_email,email=ticket.activation_email)
            tid_url = 'http://' + request.get_host()
            tid_url = tid_url + '/t/'
            tid_url = tid_url + str(ticket.id)
            Owly = owly_api.Owly()
            response = Owly.url_shorten(tid_url)
            ticket.hash = response['results']['hash']
            pt = Ticket.objects.get(id=request.POST.get('parent_ticket_id'))
            ticket.parent_ticket = pt
            ticket.save()
            url = response['results']['shortUrl']
            status = 'new'
        except Ticket.MultipleObjectsReturned:
            return render(request, '500.html', { 'message':'Multiple Objects Returned!'})
        response_dict = {}
        response_dict.update({'hash': ticket.hash,'url':url,'status':status  })
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

def zeroclicktest(request):
    return render(request, 'zeroclicktest.html')