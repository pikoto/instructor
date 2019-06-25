from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'questsions.views.QuestionsCategory', name='QuestionsCategory'),

    url(r'category/conf/$', 'questsions.views.QuestCategoryConf', name='QuestCategoryConf'),
    url(r'category/add/$', 'questsions.views.QuestCategoryAdd', name='QuestCategoryAdd'), 
    url(r'category/set/(?P<name>[a-z-0-9]+)/(?P<num>[0-9]+)/$', 'questsions.views.QuestCategorySetActive', name='QuestCategorySetActive'),
    url(r'category/del/(?P<name>[a-z-0-9]+)/$', 'questsions.views.QuestCategoryDel', name='QuestCategoryDel'),        
    url(r'category/edit/(?P<name>[a-z-0-9]+)/$', 'questsions.views.QuestCategoryEdit', name='QuestCategoryEdit'),        

    url(r'answer/conf/$', 'questsions.views.QuestAnswerConf', name='QuestAnswerConf'),
    url(r'answer/(?P<name>[0-9]+)/add/$', 'questsions.views.QuestAnswerAdd', name='QuestAnswerAdd'), 
    url(r'answer/set/(?P<name>[0-9]+)/$', 'questsions.views.QuestAnswerSetActive', name='QuestAnswerSetActive'),
    url(r'answer/del/(?P<name>[0-9]+)/$', 'questsions.views.QuestAnswerDel', name='QuestAnswerDel'), 
    url(r'answer/edit/(?P<name>[a-z-0-9]+)/$', 'questsions.views.QuestAnswerEdit', name='QuestAnswerEdit'),        

    url(r'answer/(?P<name>[a-z-0-9]+)/$', 'questsions.views.answerForQuest', name='answerForQuest'), 


    # TODO url(r'conf/$', 'questsions.views.QuestConf', name='QuestConf'),
    url(r'(?P<name>[a-z-0-9]+)/add/$', 'questsions.views.QuestAdd', name='QuestAdd'), 
    url(r'(?P<name>[a-z-0-9]+)/quest/$', 'questsions.views.QuestionsForCat', name='QuestionsForCat'),
    url(r'set/(?P<name>[a-z-0-9]+)/(?P<num>[0-9]+)/$', 'questsions.views.QuestSetActive', name='QuestSetActive'),
    url(r'del/(?P<name>[0-9]+)/$', 'questsions.views.QuestDel', name='QuestDel'),      
    
      
]
    