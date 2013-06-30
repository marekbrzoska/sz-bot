from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('bot.gui.views',
    (r'^$',          'index'),
    (r'^add/$',      'new'),
    #(r'^done_add/$', 'add'),
    #(r'^del/$',      'del_view'),
    #(r'^done_del/$', 'del'),
    # Example:
    # (r'^bot/', include('bot.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
