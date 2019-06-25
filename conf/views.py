from django.template import RequestContext
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django import forms

from django.db import connection, transaction
from itertools import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.template import Library
from django.template.defaultfilters import stringfilter


register = Library()
IGNORE_METHODS = ['join']

from conf.models import Config_dc, RegisterConfig_dc_items, MessageConfig_dc_items
from applications.forms import UserForm, UserProfileForm, MessageForm
from applications.views import template, footer_dc

# Create your views here.

def pagination_conf(request):
    
    contact_list = get_list_or_404(Config_dc, active = 1)
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


def ConfigIndex(request):
    
    context = RequestContext(request)

    pag = pagination_conf(request)

    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag }
    
    return render_to_response(( template() + '/conf/conf.html'), dict,  context)

def ConfRegister(request):
    
    context = RequestContext(request)
    
    conf_dc = get_list_or_404(RegisterConfig_dc_items)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'conf_dc' : conf_dc }
   
    return render_to_response(( template() + '/conf/confRegister.html'), dict,  context)

def ConfRegisterSet(request, name):

    n = name
    current = get_object_or_404(RegisterConfig_dc_items, active = 1)
    sets = get_object_or_404(RegisterConfig_dc_items, name = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/conf/register/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            current._setActiveFalse()
            current.save()
            sets._setActiveTrue()
            sets.save()
        else:
            return HttpResponseRedirect('/conf/register/')
   
    return HttpResponseRedirect('/conf/register/')


def pagination_message(request):
    
    contact_list = get_list_or_404(MessageConfig_dc_items, deleted=0)
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page

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


def ConfMessage(request):
    context = RequestContext(request)
    
    pag = pagination_message(request)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag }
   
    return render_to_response(( template() + '/conf/confMessage.html'), dict,  context)


def AddMessage(request):
    context = RequestContext(request)
    
    #conf_dc = get_list_or_404(MessageConfig_dc_items)
    add = 0
    message_form = MessageForm()
    er = []
    
    
    if request.method == 'POST':
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message._setAdd(request.user)
            message.save()
            add = 1
        else:
            er.append(message_form.errors)

    dict = {'template': template(), 'footer_dc' : footer_dc(), 'message_form' : message_form, 'er' : er, 'add' : add }
   
    return render_to_response(( template() + '/conf/addMessage.html'), dict,  context)


def ConfMessageSetActive(request, name, num):

    n = name
    current = get_object_or_404(MessageConfig_dc_items, id = n)
    sets = get_object_or_404(MessageConfig_dc_items, id = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/conf/message/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            if current.active:
                sets._setActiveFalse()
                sets.save()
            else:
                sets._setActiveTrue()
                sets.save()
        else:
            return HttpResponseRedirect('/conf/message/')  
    
    return HttpResponseRedirect('/conf/message/?page='+num)     


def EditMessage(request, name):
    
    context = RequestContext(request)

    dict = {'template': template(), 'footer_dc' : footer_dc()}

    return render_to_response(( template() + '/conf/addMessage.html'), dict,  context)


def ConfMessageDel(request, name):

    n = name
    sets = get_object_or_404(MessageConfig_dc_items, id = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/conf/message/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            sets._setDel(request.user)
            sets.save()
        else:
            return HttpResponseRedirect('/conf/message/')
   
    return HttpResponseRedirect('/conf/message/')      

def users(request):
    return HttpResponseRedirect('/user/')    