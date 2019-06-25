from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

from django.template.defaultfilters import slugify
from random import randint

class QuestCategory(models.Model):
    
    name =  models.TextField(max_length=128, blank=False, null=True)
    descriptions = models.TextField(blank=True, null=True)  
    
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)
    
    link = models.SlugField(unique=True, max_length=200, default='error', blank = True, null=False)
    #models.URLField(max_length=200, default='error', blank = True, null=False)
    
    add_user = models.ForeignKey(User, related_name='+')
    add_date = models.DateTimeField()

    mod_user = models.ForeignKey(User, related_name='+', null=True)
    mod_date = models.DateTimeField(blank=True, null=True)

    deleted = models.BooleanField(default=False)
    del_user = models.ForeignKey(User, related_name='+', null=True)
    del_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name
    
    def _setActiveFalse(self):
        self.active = 0  
        
    def _setActiveTrue(self):
        self.active = 1     
        
    def _setAdd(self, u):
        self.add_user = u
        self.add_date = datetime.now()
    
    def _setMod(self, u):
        self.mod_user = u
        self.mod_date = datetime.now()        
        
    def _setDel(self, u):
        self.deleted = 1
        self.active = 0         
        self.del_user = u
        self.del_date = datetime.now()
        
    def _setLink(self, n):
        slug_str = "%s %s" % (n, randint(1,100)) 
        self.link = slugify(slug_str) 
        #slugify(n.lower())  
 
        
class Question(models.Model):
    title =  models.CharField(max_length=128, blank=True, null=True) 

    quest = models.TextField(blank=True, null=True)  
    nick =  models.CharField(max_length=32, blank=True, null=True) 

    add_date = models.DateTimeField()                   
    
        
    category = models.ForeignKey(QuestCategory, related_name='+')
    
    nickId = models.PositiveIntegerField(default=0, blank=True, null=False)
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)

    link = models.SlugField(unique=True, max_length=200, default='error', blank = True, null=False)

    deleted = models.BooleanField(default=False)
    del_date = models.DateTimeField(blank=True, null=True)
    
    def _setActiveFalse(self):
        self.active = 0  
        
    def _setActiveTrue(self):
        self.active = 1     
        
    def _setAdd(self):
        #self.nick = u
        self.add_date = datetime.now()
        
    def _setDel(self):
        self.deleted = 1
        self.active = 0         
        self.del_date = datetime.now()
    
    def _setCategory(self, n):
        self.category = n
        
    def _setLink(self, n):
        slug_str = "%s %s" % (n, randint(1,100)) 
        self.link = slugify(slug_str)      
        
class QuestAnswer(models.Model):
    title =  models.CharField(max_length=128, blank=True, null=True) 

    answer = models.TextField(blank=True, null=True)  
    
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)
    
    link = models.SlugField(unique=True, max_length=200, default='error', blank = True, null=False)
    #models.URLField(max_length=200, default='error', blank = True, null=False)
    
    quest = models.ForeignKey(Question, related_name='+')
    
    add_user = models.ForeignKey(User, related_name='+')
    add_date = models.DateTimeField()

    mod_user = models.ForeignKey(User, related_name='+', null=True)
    mod_date = models.DateTimeField(blank=True, null=True)

    deleted = models.BooleanField(default=False)
    del_user = models.ForeignKey(User, related_name='+', null=True)
    del_date = models.DateTimeField(blank=True, null=True)
    
    def _setActiveFalse(self):
        self.active = 0  
        
    def _setActiveTrue(self):
        self.active = 1     
        
    def _setAdd(self, u):
        self.add_user = u
        self.add_date = datetime.now()
        
    def _setQuest(self, q):
        self.quest = q
        
    def _setDel(self, u):
        self.deleted = 1
        self.active = 0         
        self.del_user = u
        self.del_date = datetime.now()
        
    def _setLink(self, n):
        slug_str = "%s %s %s" % (n, "answer", randint(1,100)) 
        self.link = slugify(slug_str) 
        #slugify(n.lower())         
                