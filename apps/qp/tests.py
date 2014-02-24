## Owly API Test
# import owly_api
#
# Owly = owly_api.Owly()
# Owly.test_url_shorten()
# Owly.url_shorten("http://foo.com")


## Raffle draw test
import os
import sys
sys.path.append('../../')
from models import *
r = Raffle.objects.get(business=2)
r.draw()