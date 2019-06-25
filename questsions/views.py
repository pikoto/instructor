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

from models import QuestCategory, Question, QuestAnswer
from forms import CategoryForm, QuestForm, AnswerForm #, CaptchaForm
from applications.views import template, footer_dc


def getCategoryItems():
    
    items = QuestCategory.objects.filter(active=1, deleted=0)
    
    return items

def getCategoryItemsCountQuest(cat):

    quest = []
    
    for e in cat:
        k = {}
        k['id'] = e.id
        k['len'] = Question.objects.filter(active=1, deleted=0, category = e.id).count()
        quest.append(k)
        
    return quest   

def pagination_quest_category(request):
    
    u=1
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


def QuestionsCategory(request):
    context = RequestContext(request)
    
    cat = getCategoryItems()
    quest = getCategoryItemsCountQuest(cat)
    pag = pagination_quest_category(request)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag, 'quest' : quest }

    return render_to_response(( template() + '/questsions/category.html'), dict, context)


def QuestCategoryAdd(request):
    context = RequestContext(request)
    
    add = 0
    category_form = CategoryForm()
    er = []
    
    
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST)
        if category_form.is_valid():
            cat = category_form.save(commit=False)
            cat._setAdd(request.user)
            cat._setLink(cat.name)
            cat.save()
            add = 1
        else:
            er.append(category_form.errors)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'quest_form' : category_form, 'er' : er, 'add' : add}

    return render_to_response(( template() + '/questsions/addCategory.html'), dict, context)  

def pagination_quest_category_conf(request):
    
    contact_list = get_list_or_404(QuestCategory, deleted=0)
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


def QuestCategoryConf(request):
    context = RequestContext(request)
    
    pag = pagination_quest_category_conf(request)

    dict = {'template': template(), 'footer_dc' : footer_dc(), 'pag' : pag }
   
    return render_to_response(( template() + '/questsions/confCategory.html'), dict,  context)  

def QuestCategorySetActive(request, name, num):

    n = name
    current = get_object_or_404(QuestCategory, link = n)
    sets = get_object_or_404(QuestCategory, link = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/questsions/category/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            if current.active:
                sets._setActiveFalse()
                sets.save()
            else:
                sets._setActiveTrue()
                sets.save()
        else:
            return HttpResponseRedirect('/questsions/category/conf/?page='+num)  
    
    return HttpResponseRedirect('/questsions/category/conf/?page='+num)       

def QuestCategoryDel(request, name):
    
    n = name
    current = get_object_or_404(QuestCategory, link = n)
    
    if request.user.id is None:
        return HttpResponseRedirect('/questsions/category/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            current._setDel(request.user)
            current.save()
        else:
            return HttpResponseRedirect('/questsions/category/conf/')
   
    return HttpResponseRedirect('/questsions/category/conf/')    

def QuestAdd(request, name):
    
    context = RequestContext(request)

    add = 0
    quest_form = QuestForm()
    #captcha_form = CaptchaForm()
    
    er = []
    
    cat = get_object_or_404(QuestCategory, link = name)
    
    if request.method == 'POST':
        quest_form = QuestForm(data=request.POST)
        if quest_form.is_valid():
            quest = quest_form.save(commit=False)
            #quest._setAdd(request.user)
            quest._setAdd()
            quest._setCategory(cat)
            #quest._setActiveFalse()
            quest._setLink(quest.category)
            quest._setActiveTrue()
            quest.save()
            add = 1
        else:
            er.append(quest_form.errors)


    dict = {'template': template(), 'footer_dc' : footer_dc(), 'quest_form' : quest_form, 'er' : er, 'add' : add, 'cat' : cat}

    return render_to_response(( template() + '/questsions/addQuest.html'), dict,  context)      



def pagination_quest_for_category(request, list):
    
    contact_list = list
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

def QuestionsForCat(request, name):
    context = RequestContext(request)
    
    cat = get_object_or_404(QuestCategory, link = name)
    answer_items=[]
    if request.user.id is None:
        quest_items = Question.objects.filter(active = 1, deleted = 0, category = cat)
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            quest_items = Question.objects.filter(deleted = 0, category = cat)
            for e in quest_items:
                k={}
                k['quest_id'] = e.id
                k['answer'] = QuestAnswer.objects.filter(deleted = 0, quest = e.id)
                answer_items.append(k)
            #getAnswerForQuest_items(quest_items)
        else:
            quest_items = Question.objects.filter(active = 1, deleted = 0, category = cat)
            for e in quest_items:
                k={}
                k['quest_id'] = e.id
                k['answer'] = QuestAnswer.objects.filter(deleted = 0, quest = e.id)
                answer_items.append(k)
                
    pag = pagination_quest_for_category(request, quest_items)            
                            
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'cat' : cat, 'pag' : pag, 'answer_items' : answer_items }

    return render_to_response(( template() + '/questsions/questionsForCat.html'), dict,  context)   

def QuestDel(request, name):
    
    n = name
    current = get_object_or_404(Question, id = n)
    
    link = current.category.link
    
    if request.user.id is None:
        return HttpResponseRedirect('/questsions/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            current._setDel()
            current.save()
        else:
            return HttpResponseRedirect('/questsions/' + link + '/quest/')
   
    return HttpResponseRedirect('/questsions/' + link + '/quest/')      

def QuestSetActive(request, name, num):
    
    n = name
    current = get_object_or_404(Question, id = n)
    
    link = current.category.link
    
    if request.user.id is None:
        return HttpResponseRedirect('/questsions/')
    else:
        if request.user.is_authenticated and request.user.userprofile.status.id == 1:
            if current.active:
                current._setActiveFalse()
                current.save()
            else:
                current._setActiveTrue()
                current.save()
        else:
            return HttpResponseRedirect('/questsions/' + link + '/quest/?page='+num)
   
    return HttpResponseRedirect('/questsions/' + link + '/quest/?page='+num)         

def QuestAnswerEdit(request, name):

    context = RequestContext(request)
    n = name
    ed = 0
    answer_form = AnswerForm()
    er = []
    edit = get_object_or_404(QuestAnswer, link = n)
    quest = get_object_or_404(Question, id = edit.quest_id)

    if request.method == 'POST':
        answer_form = AnswerForm(data=request.POST)
        if answer_form.is_valid():
            #edit = answer_form.save(commit=False)
            edit.answer = request.POST['answer']             
            edit._setAdd(request.user)
            #quest._setActiveFalse()
            edit._setLink(quest.link)
            edit._setActiveTrue()
            edit._setQuest(quest)
            edit.save()
            ed = 1
        else:
            er.append(answer_form.errors)

    dict = {'template': template(), 'footer_dc' : footer_dc(), 'answer_form' : answer_form, 'er' : er, 'ed': ed, 'edit' : edit, 'quest' : quest }

    return render_to_response(( template() + '/questsions/editAnswer.html'), dict,  context)     


def QuestAnswerAdd(request, name): 
    
    context = RequestContext(request)
    n = name
    add = 0
    answer_form = AnswerForm()
    er = []
    
    quest = get_object_or_404(Question, id = n)

    if request.method == 'POST':
        answer_form = AnswerForm(data=request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer._setAdd(request.user)
            #quest._setActiveFalse()
            answer._setLink(quest.link)
            answer._setActiveTrue()
            answer._setQuest(quest)
            answer.save()
            add = 1
        else:
            er.append(answer_form.errors)

    dict = {'template': template(), 'footer_dc' : footer_dc(), 'answer_form' : answer_form, 'er' : er, 'add' : add, 'quest' : quest }

    return render_to_response(( template() + '/questsions/addAnswer.html'), dict,  context)     

def answerForQuest(request, name):
    context = RequestContext(request)
    
    n = name

    answer = get_object_or_404(QuestAnswer, link = n)
    quest = get_object_or_404(Question, id = answer.quest.id )

    dict = {'template': template(), 'footer_dc' : footer_dc(), 'answer' : answer, 'quest' : quest }

    return render_to_response(( template() + '/questsions/answerForQuest.html'), dict,  context)     

def QuestCategoryEdit(request, name):
    
    context = RequestContext(request)
    
    edit = get_object_or_404(QuestCategory, link = name)
    ed = 0
    category_form = CategoryForm()
    er = []
    
    if request.method == 'POST':
        category_form = CategoryForm(data=request.POST)
        if category_form.is_valid():
            #edit = category_form.save(commit=False)

            edit.name = request.POST['name']
            edit.descriptions = request.POST['descriptions']
            edit.status = request.POST['status']  
            
            edit._setAdd(request.user)
            edit._setLink(request.POST['name'])
            
            if 'active' in request.POST:
                edit._setActiveTrue()
            else:
                edit._setActiveFalse()
                
            edit.save()
            ed = 1
        else:
            er.append(category_form.errors)
    
    dict = {'template': template(), 'footer_dc' : footer_dc(), 'quest_form' : category_form, 'er' : er, 'ed' : ed, 'edit': edit}

    return render_to_response(( template() + '/questsions/editCategory.html'), dict, context)     