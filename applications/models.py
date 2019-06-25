from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

class Themes(models.Model):
    name = models.URLField(blank=False, null=False)
    descriptions = models.CharField(max_length=30)

    defaults = models.BooleanField(default=True)
    
    add_user = models.ForeignKey(User, related_name='+')
    add_date = models.DateTimeField()

    deleted = models.BooleanField(default=False)
    del_user = models.ForeignKey(User, related_name='+', null=True)
    del_date = models.DateTimeField(blank=True, null=True)
    
class Themes_dc(models.Model):
    themes = models.ForeignKey(Themes, related_name='+')
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=128, blank=False, null=False)
    
class Themes_dc_items(models.Model):
    themes_dc = models.ForeignKey(Themes_dc, related_name='+')
    name =  models.TextField(max_length=128, blank=False, null=True)
    value =  models.TextField(max_length=128, blank=False, null=True)  
    parms =  models.CharField(max_length=128, blank=True, null=True) 
    
class UserStatus_dc(models.Model):
    status = models.BigIntegerField(blank=False, null=False)
    description = models.CharField(max_length=128, blank=False, null=False)
    active = models.BooleanField(default=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True, null=True)
    avatar = models.ImageField(upload_to='static/profile_images', blank=True, null=True)
    status = models.ForeignKey(UserStatus_dc, related_name='+', blank=True, null=False)
    descriptions = models.TextField(blank=True, null=True)  
    
    def __unicode__(self):
        return self.user.username
    
    def _setStatus(self, s):
        self.status = s             
 