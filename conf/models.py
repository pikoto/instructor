from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

# Create your models here.
       
class Config_dc(models.Model):
    name_table = models.TextField(max_length=128, blank=False, null=True)
    names = models.CharField(max_length=128, blank=False, null=True)
    param = models.CharField(max_length=128, blank=False, null=True)
    mod = models.CharField(max_length=128, blank=False, null=True)
    descriptions = models.TextField(blank=True, null=True)  
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)    
        
class RegisterConfig_dc_items(models.Model):
    name = models.TextField(max_length=128, blank=False, null=True)
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)
    
    def _setActiveFalse(self):
        self.active = 0  
        
    def _setActiveTrue(self):
        self.active = 1          
    
class MessageConfig_dc_items(models.Model):
    title = models.CharField(max_length=128, blank=False, null=True)
    message = models.TextField(blank=False, null=True)
    
    param = models.CharField(max_length=128, blank=False, null=True)    
    status = models.PositiveIntegerField(default=0, blank=True, null=False)
    active = models.BooleanField(default=True)
    
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    mod_user = models.ForeignKey(User, related_name='+', null=True)
    mod_date = models.DateTimeField(blank=True, null=True)
    
    add_user = models.ForeignKey(User, related_name='+')
    add_date = models.DateTimeField()

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
        
    def _setDel(self, u):
        self.deleted = 1
        self.active = 0         
        self.del_user = u
        self.del_date = datetime.now()
    
    def _setDate(self):
        self.start_date = datetime.now()
        self.end_date = datetime.now()
        
    def _setAll(self, u):
        self.add_user = u
        self.add_date = datetime.now()
