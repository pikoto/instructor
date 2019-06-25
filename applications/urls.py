from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
  #  url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'applications.views.index', name='index'),
    url(r'login/$', 'applications.views.login_user', name='login_user'),
    url(r'logout/$', 'applications.views.logout_user', name='logout_user'),
    url(r'^register/$', 'applications.views.register_user', name='register_user'), 
    
    url(r'^user/$', 'applications.views.view_user', name='view_user'), 
    url(r'^user/edit/(?P<name>[a-z-0-9]+)$', 'applications.views.edit_user', name='edit_user'), 
    url(r'^user/self/(?P<name>[a-z-0-9]+)$', 'applications.views.edit_self_user', name='edit_self_user'), 
    url(r'^user/active/(?P<name>[0-9]+)/(?P<num>[0-9]+)/$', 'applications.views.UserSetActive', name='UserSetActive'), 
    url(r'^user/deleted/(?P<name>[0-9]+)/$', 'applications.views.UserSetDeleted', name='UserSetDeleted'), 
    url(r'^user/add/$', 'applications.views.add_user', name='add_user'), 
    
    

    url(r'^questsions/', include('questsions.urls')),
    url(r'^conf/', include('conf.urls')),
    url(r'^publications/', include('publications.urls')),
    
  
    
)
