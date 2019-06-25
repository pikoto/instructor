from applications.models import UserProfile 
from conf.models import MessageConfig_dc_items
from django.contrib.auth.models import User
from django import forms

from recaptchawidget.fields import ReCaptchaField 


class UserForm(forms.ModelForm):
    recaptcha = ReCaptchaField()
    
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'avatar')
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageConfig_dc_items
        fields = ('title', 'message', 'param', 'status', 'active', 'start_date', 'end_date'  )   
        # 
        
        
        
        
        
            