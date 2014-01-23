from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

class Business(models.Model):
    auth_user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length="64")
    contact_person = models.CharField(max_length="64")
    contact_phone = models.CharField(max_length="12")
    address = models.CharField(max_length="64")
    def __unicode__(self):
        return self.name



