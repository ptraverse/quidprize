from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^business/$', 'apps.qp.views.business'),
    url(r'^log_in/$','apps.qp.views.log_in'),
    url(r'^log_out/$','apps.qp.views.log_out'),
    url(r'^register/$','apps.qp.views.register'),

    url(r'^$','apps.qp.views.index'),
	
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
