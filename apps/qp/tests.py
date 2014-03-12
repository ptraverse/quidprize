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
t = Ticket.objects.create(raffle=r,hash=r.business.root_ticket_name())

# 4. simulate ticket clicks
# 5. simulate ticket creation
# 6. simulate more ticket clicks, creation
# 7. simulate draw
# 8. simulate win
