from publications.models import PubCategory, PubPublications, PubAttachments
from django.contrib.auth.models import User
from django import forms

#from recaptchawidget.fields import ReCaptchaField 


class PubCategoryForms(forms.ModelForm):
    #recaptcha = ReCaptchaField()
    
    class Meta:
        model = PubCategory
        fields = ('name', 'descriptions', 'status', 'active' )
        
        
class PubPublicationsForms(forms.ModelForm):  
    
    class Meta:
        model = PubPublications
        fields = ('name', 'descriptions', 'category', 'active' )
   
class PubAttatchemntsForms(forms.ModelForm):  
    
    class Meta:
        model = PubAttachments
        fields = ('name', 'descriptions', 'files' )