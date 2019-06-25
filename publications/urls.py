from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'publications.views.PubCategoryIndex', name='PubCategoryIndex'),
    url(r'cat/(?P<name>[0-9-a-z]+)/$', 'publications.views.PubForCategory', name='PubForCategory'),
    url(r'pub/(?P<name>[0-9-a-z]+)/$', 'publications.views.PubPublicationsItem', name='PubPublicationsItem'),

    url(r'category/conf/$', 'publications.views.ConfPubCategory', name='ConfPubCategory'),
    url(r'category/add/$', 'publications.views.AddPubCategory', name='AddPubCategory'), 
    url(r'category/set/(?P<name>[a-z-0-9]+)/(?P<num>[0-9]+)/$', 'publications.views.PubCategorySetActive', name='PubCategorySetActive'),
    url(r'category/del/(?P<name>[a-z-0-9]+)/$', 'publications.views.PubCategoryDel', name='PubCategoryDel'),        
    url(r'category/edit/(?P<name>[a-z-0-9]+)/$', 'publications.views.PubCategoryEdit', name='PubCategoryEdit'),        
 
    url(r'conf/$', 'publications.views.ConfPubPublications', name='ConfPubPublications'),
    url(r'add/$', 'publications.views.AddPubPublications', name='AddPubPublications'), 
    url(r'set/(?P<name>[a-z-0-9]+)/(?P<num>[0-9]+)/$', 'publications.views.PubPublicationsSetActive', name='PubPublicationsSetActive'),
    url(r'del/(?P<name>[a-z-0-9]+)/$', 'publications.views.PubPublicationsDel', name='PubPublicationsDel'),        
    url(r'edit/(?P<name>[a-z-0-9]+)/$', 'publications.views.PubPublicationsEdit', name='PubPublicationsEdit'), 

    url(r'attatchemts/(?P<name>[a-z-0-9]+)/$', 'publications.views.PubAttatchemntsConf', name='PubAttatchemntsConf'), 
    url(r'attatchemts/add/(?P<name>[a-z-0-9]+)/$', 'publications.views.AddPubAttatchments', name='AddPubAttatchments'), 
    url(r'attatchemts/set/(?P<name>[a-z-0-9]+)/$', 'publications.views.PubAttatchmentsSetActive', name='PubAttatchmentsSetActive'),
    url(r'attatchemts/(?P<name>[a-z-0-9]+)/del/$', 'publications.views.PubAttatchmentsDel', name='PubAttatchmentsDel'),            
    
    
      
]
  