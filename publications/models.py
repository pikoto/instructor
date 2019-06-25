from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

from django.template.defaultfilters import slugify
from random import randint

from django.shortcuts import get_object_or_404

class PubCategory(models.Model):
    
    name =  models.TextField(max_length=128, blank=False, null=True)
    descriptions = models.TextField(blank=True, null=True)  
    
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)

    temporary = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    
    link = models.SlugField(unique=True, max_length=200, default='error', blank = True, null=False)
    
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

    def _setTemporaryFalse(self):
        self.temporary = 0  
        
    def _setTemporaryTrue(self):
        self.temporary = 1  
                
    def _setDate(self):
        self.start_date = datetime.now()
        self.end_date = datetime.now()

class PubPublications(models.Model):
    
    name =  models.TextField(max_length=128, blank=False, null=True)
    descriptions = models.TextField(blank=True, null=True)  
    
    temporary = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
        
    category = models.ForeignKey(PubCategory, related_name='+')
    
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)
    
    link = models.SlugField(unique=True, max_length=200, default='error', blank = True, null=False)
    
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

    def _setTemporaryFalse(self):
        self.temporary = 0  
        
    def _setTemporaryTrue(self):
        self.temporary = 1  
                
    def _setDate(self):
        self.start_date = datetime.now()
        self.end_date = datetime.now()         

class PubTypesAttachments(models.Model):
    
    name =  models.TextField(max_length=128, blank=False, null=True)
    descriptions = models.TextField(blank=True, null=True)  
    active = models.BooleanField(default=True)
    icons = models.TextField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name
    
    def _setActiveFalse(self):
        self.active = 0  
        
    def _setActiveTrue(self):
        self.active = 1  
     
    def _setType(self, n, d):
        self.name = n
        self.desctiptions = d 
                
class PubAttachments(models.Model):
    
    name =  models.TextField(max_length=128, blank=False, null=True)
    descriptions = models.TextField(blank=True, null=True)  
    files = models.FileField(upload_to='static/pub_attachments', blank=True, null=True)
    types = models.ForeignKey(PubTypesAttachments, related_name='+')
    
    pub = models.ForeignKey(PubPublications, related_name='+')
    
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)
    
    link = models.SlugField(unique=True, max_length=200, default='error', blank = True, null=False)
    
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
