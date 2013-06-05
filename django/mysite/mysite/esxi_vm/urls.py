from django.conf.urls import patterns, include, url

urlpatterns = patterns('mysite.esxi_vm.views',
    (r'^$', 'index'),
)
