from models import QuestCategory, Question, QuestAnswer
from django.contrib.auth.models import User
from django import forms


from recaptchawidget.fields import ReCaptchaField 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = QuestCategory
        fields = ('name', 'descriptions', 'status', 'active' )
        
class QuestForm(forms.ModelForm):
    recaptcha = ReCaptchaField()
    class Meta:
        model = Question
        fields = ('title', 'quest', 'nick' )      
        
class AnswerForm(forms.ModelForm):    
    class Meta:
        model = QuestAnswer
        fields = ('title', 'answer' )  