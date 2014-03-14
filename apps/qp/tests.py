## Owly API Test
# import owly_api
#
# Owly = owly_api.Owly()
# Owly.test_url_shorten()
# Owly.url_shorten("http://foo.com")


## Raffle draw test
# import os
# import sys
#
# sys.path.append('../../')
# from models import *
# r = Raffle.objects.get(business=2)
# r.draw()


## Email Test
# import local_settings_development
# from django.core.mail import EmailMessage
# email = EmailMessage('Mail Test', 'This is a test', to=['philippe.traverse@gmail.com'])
# email.send()


## Demo
#
from apps.qp.models import *

# 1. initialize user
try:
    u = User.objects.get(username='testunit_user')
except Exception:
    u = User.objects.create(username='testunit_user')
print(u)

# 2a. initialize business by user
try:
    b = Business.objects.get(name='testunit_business')
except Exception:
    b = Business.objects.create(auth_user=u,name='testunit_business')
print(b)
# 2b. initialize raffle by business
try:
    r = Raffle.objects.create(business=b,target_url='http://testunit_url.com/',date_created=datetime.now(),expiry_date=datetime.now())
except Exception:
    print('couldnt create raffle')
    exit()
print(r)

# 3. init root ticket
t = Ticket.objects.create_ticket(raffle=r,is_root_ticket=True)

# 4. simulate ticket clicks
import requests
url_base = "http://bit.ly/"
url_ending = t.hash
print url_base+url_ending
req = requests.get(url_base+url_ending)
print('<<<')
print(req.text[0:128])
print('... >>>')

#4.5 Check that those links are getting counted
print(t.hash+' has ')
print(t.get_num_clicks())
print('clicks')

# 5. simulate ticket creation
t2 = Ticket.objects.create_ticket(raffle=r,is_root_ticket=False,parent_ticket=t)
t3 = Ticket.objects.create_ticket(raffle=r,is_root_ticket=False,parent_ticket=t2)
t4 = Ticket.objects.create_ticket(raffle=r,is_root_ticket=False,parent_ticket=t3)

# 6. simulate more ticket clicks, creation
ticketlist = Ticket.objects.all()
for tx in ticketlist:
    url_ending = tx.hash
    r = requests.get(url_base+url_ending)
    print('<<<')
    print(r.text[0:128])
    print('... >>>\n')


# 7. simulate draw
# 8. simulate win
