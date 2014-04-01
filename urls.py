from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^b/(.*)$', 'apps.qp.views.business'),
    url(r'^beta_new_raffle/$', 'apps.qp.views.beta_new_raffle'),
    url(r'^business_create/$', 'apps.qp.views.business_create'),
    url(r'^completion_logger/$', 'apps.qp.views.completion_logger'),
    url(r'^log_in/$','apps.qp.views.log_in'),
    url(r'^log_out/$','apps.qp.views.log_out'),
    url(r'^raffle/$','apps.qp.views.raffle'),
    url(r'^raffles/$','apps.qp.views.raffles'),
    url(r'^raffle_div_test/(.*)/$','apps.qp.views.raffle_div_test'),
    url(r'^register/$','apps.qp.views.register'),
    url(r'^sigma_gexf/(.*)/$','apps.qp.views.sigma_gexf'),
    url(r'^ticket_create/$','apps.qp.views.ticket_create'),
    url(r'^tid/(.*)/$','apps.qp.views.ticket_id'),
    url(r'^tr/(.*)$','apps.qp.views.ticket_redirect'),
    url(r'^t/(.*)$','apps.qp.views.ticket_redirect'),
    url(r'^thanks/$','apps.qp.views.thanks'),
    url(r'^tickets/$','apps.qp.views.tickets'),
    url(r'^ticket_activation/(.*)/$','apps.qp.views.ticket_activation'), # change this to something nice later
    url(r'^ticket_activation_json/(.*)/$','apps.qp.views.ticket_activation_json'), # change this to something nice later
    url(r'^(\w+)$','apps.qp.views.ticket_by_hash'),
    url(r'^$','apps.qp.views.index'),


    #only in development!
    url(r'^list/$', 'apps.qp.views.list', name='list'),
    url(r'^countdown_test/$', 'apps.qp.views.test_countdown', name='countdown_test'),
    url(r'^sigma_test/$', 'apps.qp.views.sigma_test', name='sigma_test'),
    url(r'^sigma_test_json/$', 'apps.qp.views.sigma_test_json', name='sigma_test_json'),
    url(r'^sigma_test_gexf/$', 'apps.qp.views.sigma_test_gexf', name='sigma_test_gexf'),
    url(r'^raffle_countdown_test/$', 'apps.qp.views.raffle_countdown_test', name='raffle_countdown_test'),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG: #only in development!!
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)