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

from datetime import datetime 


register = Library()
IGNORE_METHODS = ['join']

from publications.models import PubCategory, PubPublications, PubTypesAttachments, PubAttachments
from publications.forms import PubCategoryForms, PubPublicationsForms, PubAttatchemntsForms
from applications.views import template, footer_dc


def getCategoryItems():
    
    items = PubCategory.objects.filter(active=1, deleted=0)
    
    return items


def getCategoryConfItems():
    
    items = PubCategory.objects.filter(deleted=0)
    
    return items 

def getPublicationsConfItems():
    
    items = PubPublications.objects.filter(deleted=0)
    
    return items    

def getPublicationsAttatchments():
    
    items = PubAttachments.objects.filter(deleted=0)
    
    return items       

def getPublicationsAttatchmentsForPub(name):
    
    pubs = get_object_or_404(PubPublications, link = name)
    
    items = PubAttachments.objects.filter(deleted=0, pub = pubs)
    
    return items  

def getPubForCategory(name):
    
    cat = get_object_or_404(PubCategory, link = name)
    
    pubs = PubPublications.objects.filter(category = cat.id, deleted = 0, active = 1)
    
    return pubs      
    
def pagination_pub_conf_category(request):
    
    contact_list = getCategoryConfItems()
    paginator = Paginator(contact_list, 5) # Show 25 contacts per page

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


def pagination_pub_category(request):
    
    contact_list = getCategoryItems()
    paginator = Paginator(contact_list, 5) # Show 25 contacts per page

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

def pagination_pub_for_category(request, name):
    contact_list = getPubForCategory(name)
    paginator = Paginator(contact_list, 5) # Show 25 contacts per page

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


def getAttatchmentsItemsCountPublications(pub):

    attatchmnets = []
    
    for e in pub:
        k = {}
        k['id'] = e.id
        k['len'] = PubAttachments.objects.filter(active=1, deleted=0, pub = e.id).count()
        attatchmnets.append(k)
        
    return attatchmnets   


def PubForCategory(request, name):
    context = RequestContext(request)

    pag = pagination_pub_for_category(request, name)
    cat = get_object_or_404(PubCategory, link = name)
    att = getAttatchmentsItemsCountPublications(pag)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag, 'cat' : cat, 'att' : att }

    return render_to_response(( template() + '/publications/publicationsForCategory.html'), dict, context)

def PubCategoryIndex(request):
    context = RequestContext(request)

    pag = pagination_pub_category(request)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag }

    return render_to_response(( template() + '/publications/category.html'), dict, context)


def PubPublicationsItem(request, name):
    context = RequestContext(request)

    pubs = get_object_or_404(PubPublications, link = name)
    att = PubAttachments.objects.filter(pub = pubs.id, deleted = 0, active = 1 )
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pub' : pubs, 'att' : att}

    return render_to_response(( template() + '/publications/publications.html'), dict, context)    

def ConfPubCategory(request):
    context = RequestContext(request)

    pag = pagination_pub_conf_category(request)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag }

    return render_to_response(( template() + '/publications/confCategory.html'), dict, context)

def AddPubCategory(request):
    context = RequestContext(request)
    
    add = 0
    category_form = PubCategoryForms()
    er = []
    
    if request.method == 'POST':
        category_form = PubCategoryForms(data=request.POST)
        if category_form.is_valid():
            cat = category_form.save(commit=False)
            cat._setAdd(request.user)
            cat._setLink(cat.name)
            if 'active' in request.POST:
                cat._setActiveTrue()
            else:        
                cat._setActiveFalse()

            if 'temporary' in request.POST:
                cat.start_date = request.POST['start_date'] #datetime.now()
                cat.end_date = request.POST['end_date'] #datetime.now()
            cat.save()
            add = 1
        else:
            er.append(category_form.errors)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'category_form' : category_form, 'er' : er, 'add' : add}

    return render_to_response(( template() + '/publications/addCategory.html'), dict, context)  

def PubCategorySetActive(request, name, num):

    n = name
    current = get_object_or_404(PubCategory, link = n)
    sets = get_object_or_404(PubCategory, link = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/publications/category/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            if current.active:
                sets._setActiveFalse()
                sets.save()
            else:
                sets._setActiveTrue()
                sets.save()
        else:
            return HttpResponseRedirect('/publications/category/conf/?page='+num)  
    
    return HttpResponseRedirect('/publications/category/conf/?page='+num)   

def PubCategoryDel(request, name):
    
    n = name
    current = get_object_or_404(PubCategory, link = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/publications/category/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            current._setDel(request.user)
            current.save()
        else:
            return HttpResponseRedirect('/publications/category/conf/')
   
    return HttpResponseRedirect('/publications/category/conf/')    

def PubCategoryEdit(request, name):
    
    context = RequestContext(request)
    
    edit = get_object_or_404(PubCategory, link = name)
    ed = 0
    category_form = PubCategoryForms()
    er = []
    
    if request.method == 'POST':
        category_form = PubCategoryForms(data=request.POST)
        if category_form.is_valid():
            #edit = category_form.save(commit=False)

            edit.name = request.POST['name']
            edit.descriptions = request.POST['descriptions']
            edit.status = request.POST['status']  
            
            edit._setMod(request.user)
            edit._setLink(request.POST['name'])
            
            if 'active' in request.POST:
                edit._setActiveTrue()
            else:        
                edit._setActiveFalse()

            if 'temporary' in request.POST:
                edit._setTemporaryTrue()
                edit.start_date = request.POST['start_date'] #datetime.now()
                edit.end_date = request.POST['end_date'] #datetime.now()
            else:
                edit._setTemporaryFalse()
                edit.start_date = None
                edit.end_date = None
                
            edit.save()
            ed = 1
        else:
            er.append(category_form.errors)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'category_form' : category_form, 'er' : er, 'ed' : ed, 'edit': edit}

    return render_to_response(( template() + '/publications/editCategory.html'), dict, context)     
    

def pagination_pub_conf_publications(request):
    
    contact_list = getPublicationsConfItems()
    paginator = Paginator(contact_list, 5) # Show 25 contacts per page

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

def ConfPubPublications(request):
    context = RequestContext(request)

    pag = pagination_pub_conf_publications(request)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag }

    return render_to_response(( template() + '/publications/confPublications.html'), dict, context) 


def AddPubPublications(request):
    context = RequestContext(request)
    
    cat = getCategoryItems()
    add = 0
    pub_form = PubPublicationsForms()
    er = []
    
    if request.method == 'POST':
        pub_form = PubPublicationsForms(data=request.POST)
        if pub_form.is_valid():
            pub = pub_form.save(commit=False)
            pub._setAdd(request.user)
            pub._setLink(pub.name)
            
            if 'active' in request.POST:
                pub._setActiveTrue()
            else:        
                pub._setActiveFalse()

            if 'temporary' in request.POST:
                pub._setTemporaryTrue()
                pub.start_date = request.POST['start_date'] #datetime.now()
                pub.end_date = request.POST['end_date'] #datetime.now()
                            
            pub.save()
            add = 1
        else:
            er.append(pub_form.errors)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pub_form' : pub_form, 'er' : er, 'add' : add, 'cat' : cat}

    return render_to_response(( template() + '/publications/addPublications.html'), dict, context)  

def PubPublicationsSetActive(request, name, num):

    n = name
    current = get_object_or_404(PubPublications, link = n)
    sets = get_object_or_404(PubPublications, link = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/publications/?page='+num)
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            if current.active:
                sets._setActiveFalse()
                sets.save()
            else:
                sets._setActiveTrue()
                sets.save()
        else:
            return HttpResponseRedirect('/publications/?page='+num)  
    
    return HttpResponseRedirect('/publications/conf/?page='+num)   

def PubPublicationsDel(request, name):
    
    n = name
    current = get_object_or_404(PubPublications, link = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/publications/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            current._setDel(request.user)
            current.save()
        else:
            return HttpResponseRedirect('/publications/conf/')
   
    return HttpResponseRedirect('/publications/conf/')    

def PubPublicationsEdit(request, name):
    
    context = RequestContext(request)
    cat = getCategoryItems()
    
    edit = get_object_or_404(PubPublications, link = name)
    ed = 0
    pub_form = PubPublicationsForms()
    er = []
    
    if request.method == 'POST':
        pub_form = PubCategoryForms(data=request.POST)
        if pub_form.is_valid():
            #edit = category_form.save(commit=False)

            edit.name = request.POST['name']
            edit.descriptions = request.POST['descriptions']
            
            edit._setMod(request.user)
            edit._setLink(request.POST['name'])
            
            if 'category' in request.POST:
                edit.category = get_object_or_404(PubCategory, id =request.POST['category'])
            
            if 'active' in request.POST:
                edit._setActiveTrue()
            else:        
                edit._setActiveFalse()

            if 'temporary' in request.POST:
                edit._setTemporaryTrue()
                edit.start_date = request.POST['start_date'] #datetime.now()
                edit.end_date = request.POST['end_date'] #datetime.now()
            else:
                edit._setTemporaryFalse()
                edit.start_date = None
                edit.end_date = None            
                
            edit.save()
            ed = 1
        else:
            er.append(pub_form.errors)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pub_form' : pub_form, 'er' : er, 'ed' : ed, 'edit': edit, 'cat' : cat}

    return render_to_response(( template() + '/publications/editPublications.html'), dict, context)   


def pagination_pub_conf_Attatchemnts(request, name):
    
    contact_list = getPublicationsAttatchmentsForPub(name)
    paginator = Paginator(contact_list, 5) # Show 25 contacts per page

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

def PubAttatchemntsConf(request, name):
    context = RequestContext(request)

    edit = get_object_or_404(PubPublications, link = name)

    pag = pagination_pub_conf_Attatchemnts(request, name)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag, 'edit' : edit }

    return render_to_response(( template() + '/publications/confAttatchemnts.html'), dict, context) 

def AddPubAttatchments(request, name):
    context = RequestContext(request)
    
    edit = get_object_or_404(PubPublications, link = name)
    types = get_list_or_404(PubTypesAttachments, active = 1)
    add = 0
    atta_form = PubAttatchemntsForms()
    er = []
    
    if request.method == 'POST':
        atta_form = PubAttatchemntsForms(data=request.POST)
        if atta_form.is_valid():
            atta = atta_form.save(commit=False)
            
            #_types = get_object_or_404(PubTypesAttachments, name = request.POST['types'])
            atta.types = get_object_or_404(PubTypesAttachments, id = request.POST['types'])
            atta.pub = edit
                     
            if 'active' in request.POST:
                atta._setActiveTrue()
            else:
                atta._setActiveFalse()
                
            if 'files' in request.FILES:
                atta.files = request.FILES['files']
                
            atta._setAdd(request.user)
            atta._setLink(atta.name)
            atta.save()
            add = 1
        else:
            er.append(atta_form.errors)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'atta_form' : atta_form, 'er' : er, 'add' : add, 'edit' : edit, 'types' : types}

    return render_to_response(( template() + '/publications/AddPubAttatchments.html'), dict, context)  

def PubAttatchmentsSetActive(request, name):

    current = get_object_or_404(PubAttachments, link = name)
    sets = get_object_or_404(PubAttachments, link = name)
    
    if request.user.id is None:
        return HttpResponseRedirect('/publications/?page=1')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            if current.active:
                sets._setActiveFalse()
                sets.save()
            else:
                sets._setActiveTrue()
                sets.save()
        else:
            return HttpResponseRedirect('/publications/attatchemts/'+ sets.pub.link +'/?page=1')  
    
    return HttpResponseRedirect('/publications/attatchemts/'+ sets.pub.link +'/?page=1')   

def PubAttatchmentsDel(request, name):
    
    current = get_object_or_404(PubAttachments, link = name)
    
    if request.user.id is None:
        return HttpResponseRedirect('/publications/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            current._setDel(request.user)
            current.save()
        else:
            return HttpResponseRedirect('/publications/attatchemts/'+ current.pub.link +'/?page=1')  
   
    return HttpResponseRedirect('/publications/attatchemts/'+ current.pub.link +'/?page=1')  
