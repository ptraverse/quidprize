from django.db import models
from django.contrib.auth.models import *
import os.path
from datetime import datetime
import bitly_api
import simplejson
import igraph

API_USER = "cfd992841301aabcd843e8ed4622b9c88e320e8e"
API_KEY = "c5955c440b750b215924bd08d1b79518ca4a82c4"
ACCESS_TOKEN = "1214d30c74adf88608b83bdc8eac7b053a57b6f4"

class Business(models.Model):
    auth_user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length="64")
    logo = models.FileField(upload_to='logos/')
    contact_person = models.CharField(max_length="64")
    contact_phone = models.CharField(max_length="12")
    address = models.CharField(max_length="64")
    def __unicode__(self):
        return self.name
    def root_ticket_name(self):
        root_ticket_name = self.name
        for vowel in 'aeiou':
            root_ticket_name = root_ticket_name.replace(vowel,'')
        return root_ticket_name

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    def __unicode__(self):
        filename = os.path.basename(self.docfile.name)
        return filename

class Raffle(models.Model):
    business = models.ForeignKey(Business)
    target_url = models.CharField(max_length="64")
    date_created = models.DateTimeField()
    expiry_date = models.DateTimeField()
    draw_winner = models.ForeignKey(User, null=True, blank=True)
    draw_date = models.DateTimeField(null=True)
    def __unicode__(self):
        return '100$ gift card to whoever gets as many clicks to '+self.target_url+' for '+self.business.name
    def draw(self):
        ticketlist = Ticket.objects.filter(raffle = self.id)
        total_clicks1 = 0
        for t in ticketlist:
            t.clicks = t.get_num_clicks()
            total_clicks1 = total_clicks1 + t.clicks
            t.height = t.calculate_height()
        current_height = 0
        for t in ticketlist:
            count = 0
            if t.height==current_height:
                count = count + 1
                shift = t.clicks*1.1
                sup = Ticket.objects.get(id = self.parent_ticket)
                t.clicks = t.clicks - shift
                sup.height = sup.clicks + shift
            if count==0:
                current_height = current_height + 1
        total_clicks2 = 0
        for t in ticketlist:
            total_clicks2 = total_clicks2 + t.clicks
        assert total_clicks2==total_clicks1 # throw an error if things havent been subtracted properly
        for t in ticketlist:
            c = 0
            while c<t.clicks:
                email_entries.append(t.activation_email)
        winner = random.sample(email_entries, 1)
        print winner
        self.draw_winner = winner
        self.draw_date = datetime.now()
        return winner
    def graph(self):
        g = igraph.Graph()
        tl = Ticket.objects.filter(raffle=self.id).order_by('-is_root_ticket')
        for t in tl:
            g.add_vertex(id=t.id,name=t.hash,label=t.hash)
        for t in tl:
            if t.parent_ticket_id>0:
                g.add_edge(g.vs.find(id=t.id),g.vs.find(id=t.parent_ticket_id))
        r = tl[0].id
        coords = g.layout_reingold_tilford(r,0,1) ## This is where the layout gets decided
        return coords

class TicketManager(models.Manager):
    def create_ticket(self,raffle,is_root_ticket,parent_ticket=''):
        if is_root_ticket is True:
            t = Ticket.objects.create(raffle=raffle,hash=raffle.business.root_ticket_name(),is_root_ticket=True)
        else:
            API_USER = "cfd992841301aabcd843e8ed4622b9c88e320e8e"
            API_KEY = "c5955c440b750b215924bd08d1b79518ca4a82c4"
            ACCESS_TOKEN = "1214d30c74adf88608b83bdc8eac7b053a57b6f4"
            bitly = bitly_api.Connection(access_token=ACCESS_TOKEN)
            t = self.create(raffle=raffle,is_root_ticket=False,parent_ticket=parent_ticket)
            tid_url = 'http://10.0.1.14:8000/'
            tid_url = tid_url + '/t/'
            tid_url = tid_url + str(t.id)
            response = bitly.shorten(tid_url)
            t.hash = response['hash']
            t.save()
        return t

class Ticket(models.Model):
    activation_email = models.CharField(max_length="75",null=True,default=None)
    hash = models.CharField(max_length=16,unique=True)
    raffle = models.ForeignKey(Raffle)
    is_root_ticket = models.BooleanField(default=False)
    date_activated = models.DateTimeField(null=True)
    parent_ticket = models.ForeignKey('self', null=True, blank=True)
    objects = TicketManager()
    # def stats():
    def __unicode__(self):
        return self.hash
    def get_num_clicks(self):
        if self.activation_email=='todo@allowblank.com':
            return 0
        elif self.is_root_ticket==True:
            return 0 # for now
        else:
            Bitly = bitly_api.Connection(access_token=ACCESS_TOKEN)
            return Bitly.link_clicks(link='http://bit.ly/'+self.hash)
    def calculate_height(self):
        try:
            subs = Ticket.objects.get(raffle=self.raffle, parent_ticket = self)
        except Ticket.DoesNotExist:
            return 1
        max_height = 1
        for s in subs:
            s.height = s.calculate_height()
            if s.height>max_height:
                max_height = s.height
        return max_height+1
    def completion_count(self):
        return Completion.objects.filter(ticket=self).count()

class Completion(models.Model):
	ticket = models.ForeignKey(Ticket,null=False,blank=False)
	date_inserted = models.DateTimeField(auto_now_add=True, blank=False)
	http_referer = models.CharField(max_length=64, blank=True)
	remote_addr = models.CharField(max_length=32, blank=True)
	remote_user = models.ForeignKey(User, blank=True, null=True)