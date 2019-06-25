from django.conf.urls import url


urlpatterns = [ 
    url(r'^$', 'conf.views.ConfigIndex', name='ConfigIndex'), 
    
    url(r'^register/$', 'conf.views.ConfRegister', name='ConfRegister'),
    url(r'^register/set/(?P<name>[a-z]+)/$', 'conf.views.ConfRegisterSet', name='ConfRegisterSet'),
    
    url(r'^message/$', 'conf.views.ConfMessage', name='ConfMessage'),
    url(r'^message/set/(?P<name>[0-9]+)/(?P<num>[0-9]+)/$', 'conf.views.ConfMessageSetActive', name='ConfMessageSetActive'),
    url(r'^message/add/$', 'conf.views.AddMessage', name='AddMessage'), 
    url(r'^message/del/(?P<name>[0-9]+)/$', 'conf.views.ConfMessageDel', name='ConfMessageDel'),
    
    url(r'^user/$', 'conf.views.users', name='users'),
    
 
    
    
    
]