from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'esxi/', include('mysite.esxi_vm.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
