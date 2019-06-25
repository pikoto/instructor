from django.template import RequestContext
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django import forms

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection, transaction
from itertools import *


from django.template import Library
from django.template.defaultfilters import stringfilter


register = Library()
IGNORE_METHODS = ['join']

from applications.models import Themes, Themes_dc, Themes_dc_items, UserProfile, UserStatus_dc
from applications.forms import UserForm, UserProfileForm, MessageForm

from conf.models import Config_dc, RegisterConfig_dc_items, MessageConfig_dc_items


def template():
    active = get_object_or_404(Themes, defaults=1, deleted=0)
    
    return active.name

def get_template_dc_items(names):

    dc = get_object_or_404(Themes_dc, name=names)

    if dc.active == 1:
        items = get_list_or_404(Themes_dc_items, themes_dc = dc.id)
        
        return items
    else:
        return 'null'

def get_news_dc_items():
    
    items = MessageConfig_dc_items.objects.filter(active=1, deleted=0)
    
    return items
    
def footer_dc():
    dc = get_template_dc_items("footer-social")
    
    return dc

def get_RegisterConfig_dc_active():
    
    active = RegisterConfig_dc_items.objects.get(active = 0)
    
    return active 

def get_User(ids):
    
    u = get_list_or_404(User, is_staff=0, is_superuser=0)
        
    return u

def index(request):

    context = RequestContext(request)
    
    index_dc = get_template_dc_items("index")
    news_dc = get_news_dc_items()
    footer_dc = get_template_dc_items("footer-social")
    
    dict = {'template': template(), 'index_dc' : index_dc, 'news_dc' : news_dc, 'footer_dc' : footer_dc}

    return render_to_response(( template() + '/index.html'), dict, context)

def login_user(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    
    er = []
    
    dict = {'template': template(), 'er' : er, 'footer_dc' : footer_dc()}
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                render_to_response(( template() + '/applications/login.html'), dict, context)
            else:
                # Return a 'disabled account' error message
                er.append("Twoje konto jest zablokowane")
                render_to_response(( template() + '/applications/login.html'), dict, context)
        else:
            # Return an 'invalid login' error message.
            er.append( "Bledne logowanie")
            render_to_response(( template() + '/applications/login.html'), dict, context)

    return render_to_response(( template() + '/applications/login.html'), dict, context)


def logout_user(request):
    # Since we know the user is logged in, we can now just log them out.
    
    logout(request)
    
    return HttpResponseRedirect('/#')

def register_user(request):

    context = RequestContext(request)
 
    registered = False
    er = []
    
    config = get_RegisterConfig_dc_active()
    
    if config.status == 1:
        
        if request.method == 'POST':
            user_form = UserForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)
     
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
     
                user.set_password(user.password)
                user.is_active = 0      
                user.save()
     
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.status_id = '4'
                 
                if 'avatar' in request.FILES:
                    profile.avatar = request.FILES['avatar']
                profile.save()
    
                registered = True
            else:
                user_form = UserForm()
                profile_form = UserProfileForm()
    
        user_form = UserForm()
        profile_form = UserProfileForm()
        dict = {'template': template(), 'footer_dc' : footer_dc(), 'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'conf' : config.status}
    
        return render_to_response(( template() + '/applications/register.html'), dict,  context)
    else:
        dict = {'template': template(), 'footer_dc' : footer_dc(), 'conf' : config.status}
        return render_to_response(( template() + '/applications/register.html'), dict,  context)


def pagination_user(request):
    
    u=1
    contact_list = get_User(u)
    paginator = Paginator(contact_list, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    
    return contacts
    
def view_user(request):
    context = RequestContext(request)
        
    pag = pagination_user(request)

    dict = {'template': template(), 'pag' : pag}

    return render_to_response(( template() + '/applications/user.html'), dict, context)

def add_user(request):
    
    context = RequestContext(request)
 
    add = False
    er = []
    
    status = UserStatus_dc.objects.filter(active = 1)
    
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
 
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
 
            user.set_password(user.password)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']    
            user.is_active = 0      
            user.save()
 
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.status_id = request.POST['status_id']
            profile.descriptions = request.POST['description']             
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()

            add = True
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()

    user_form = UserForm()
    profile_form = UserProfileForm()
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'user_form': user_form, 'profile_form': profile_form, 'add': add, 'status': status }

    return render_to_response(( template() + '/applications/addUser.html'), dict,  context)
    

def edit_user(request, name):
    
    context = RequestContext(request)
    
    ed = False
    er = []
    
    status = UserStatus_dc.objects.filter(active = 1)
    edit = User.objects.get(username = name)
       
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        edit1 = User.objects.get(id=edit.id)
        prof1 = UserProfile.objects.get(user_id = edit.id)
        
        edit1.first_name = request.POST['first_name']
        edit1.last_name = request.POST['last_name']
        edit1.email = request.POST['email']

        prof1.website = request.POST['website']
        prof1.status_id = request.POST['status_id']
        prof1.descriptions = request.POST['description']

        if 'avatar' in request.FILES:
            prof1.avatar = request.FILES['avatar']
        prof1.save()
        
        edit1.save()    
        prof1.save()        
        
        ed = True

    dict = {'template': template(), 'footer_dc' : footer_dc(), 'ed': ed, 'status':status, 'edit':edit }

    return render_to_response(( template() + '/applications/editUser.html'), dict,  context)    


def edit_self_user(request, name):
    
    context = RequestContext(request)
    
    ed = False
    er = []
    
    status = UserStatus_dc.objects.filter(active = 1)
    edit = User.objects.get(username = name)
       
    if request.method == 'POST':
        if request.user.id != edit.id:
            ed = False
            er.append( "Nie masz uprawnien")            
        else:
            user_form = UserForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)
            edit1 = User.objects.get(id=edit.id)
            prof1 = UserProfile.objects.get(user_id = edit.id)
            
            edit1.first_name = request.POST['first_name']
            edit1.last_name = request.POST['last_name']
            edit1.email = request.POST['email']
    
            prof1.website = request.POST['website']
            prof1.status_id = edit1.userprofile.status.status
            prof1.descriptions = request.POST['description']
    
            if 'avatar' in request.FILES:
                prof1.avatar = request.FILES['avatar']
            prof1.save()
            
            edit1.save()    
            prof1.save()                  
        
            ed = True

    dict = {'template': template(), 'footer_dc' : footer_dc(), 'ed': ed, 'status':status, 'edit':edit }

    return render_to_response(( template() + '/applications/editSelfUser.html'), dict,  context)  


def UserSetActive(request, name, num):
    
    n = name
    current = get_object_or_404(User, id = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/user/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            if current.is_active == 1:
                current.is_active=0
                current.save()
            else:
                current.is_active=1
                current.save()
        else:
            return HttpResponseRedirect('/user/')
   
    return HttpResponseRedirect('/user/?page='+num)    


def UserSetDeleted(request, name):
    
    n = name
    
    if request.user.id is None:
        return HttpResponseRedirect('/user/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            User.objects.filter(id=n).delete()
        else:
            return HttpResponseRedirect('/user/')
    
    return HttpResponseRedirect('/user/')



    
