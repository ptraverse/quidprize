from django.db import models
from django.contrib.auth.models import *
import os.path
from datetime import datetime

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
    #draw - foreign key
    def __unicode__(self):
        return '100$ gift card to whoever gets as many clicks to '+self.target_url+' for '+self.business.name

class Ticket(models.Model):
    activation_email = models.CharField(max_length="75")
    owly_hash = models.CharField(max_length="16")
    raffle = models.ForeignKey(Raffle)
    date_activated = models.DateTimeField()
    # def stats():
    def __unicode__(self):
        return self.owly_hash


