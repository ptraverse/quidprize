from django.db import models
from django.contrib.auth.models import *
import os.path
from datetime import datetime
import bitly_api

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

class Ticket(models.Model):
    activation_email = models.CharField(max_length="75")
    hash = models.CharField(max_length="16")
    raffle = models.ForeignKey(Raffle)
    date_activated = models.DateTimeField()
    parent_ticket = models.ForeignKey('self', null=True, blank=True)
    # def stats():
    def __unicode__(self):
        return self.hash
    def get_num_clicks(self):
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

