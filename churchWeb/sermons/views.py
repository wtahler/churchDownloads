from django.utils import simplejson as json
from sermons.models import *
from django.template.loader import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from churchWeb.sermons.forms import SermonFileForm, FolderForm
from churchWeb.sermons.models import *

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as djangoLogin, logout as djangoLogout, \
authenticate

import random
import math
from datetime import timedelta

def main(request,id=False):
    context = {}
    if id:
        context['allFiles'] = SermonFile.objects.filter(fileFolders=Folder.objects.get(pk=id))
        context['allFolders'] = Folder.objects.filter(folder=Folder.objects.get(pk=id))
        upFolder = Folder.objects.get(pk=id).folder
        if upFolder:
            context['currID'] = upFolder.pk
        else:
            context['currID'] = 0
    else:
        context['allFiles'] = SermonFile.objects.filter(fileFolders=None)
        context['allFolders'] = Folder.objects.filter(folder=None)
    return render_to_response('index.html',context,context_instance=RequestContext(request))

def login(request):
    context={}
    context.update(csrf(request))
    if request.method=='POST': # if data was posted, attempt to log user in
        # try to authenticate user using given username and password
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None: # if user is logged in, log them in with django's auth system
            djangoLogin(request,user)
            # redirect to whatever url the user was trying to access
            #return HttpResponseRedirect(request.POST['next'])
        else:
            context['error'] ='Username or password was incorrect'
        #return HttpResponse(json.dumps(output))
    return render_to_response('login.html',context,context_instance=RequestContext(request))

@login_required
def uploadSermon(request):
    context = {}
    context.update(csrf(request))
    context['sermonFileForm'] = SermonFileForm()
    if request.method == 'POST':
        sermonForm = SermonFileForm(request.POST,request.FILES)
        if sermonForm.is_valid():
            newSermon = sermonForm.save(commit=False)
            newSermon.owner = request.user
            newSermon.save()
            return HttpResponseRedirect(reverse(uploadSermon))
        else:
            context['sermonFileForm'] = sermonForm
            context['error'] = "Correct the errors before submitting"
    return render_to_response('sermonForm.html',context,context_instance=RequestContext(request))

@login_required
def editFolder(request,id=False):
    context = {}
    context.update(csrf(request))
    if request.method == 'POST':
        folderForm = FolderForm(request.POST)
        if folderForm.is_valid() and not id:
            folderForm = folderForm.save(commit=False)
            if id:
                folderForm.pk = id
            folderForm.save_m2m()
            folderForm.save()   
            id = folderForm.pk             
            return HttpResponseRedirect(reverse(viewFolder,args=[id]))
        elif id:
            folder = FolderForm(request.POST,instance=Folder.objects.get(pk=id)).save(commit=False)
            folder.save_m2m()
            folder.save()
            return HttpResponseRedirect(reverse(viewFolder,args=[id]))
        else:
            context['folderForm'] = folderForm
            context['error'] = "Correct the errors before submitting"
    else:
        if id:
            context['folderForm'] = FolderForm(instance=Folder.objects.get(pk=id))
            context['currID'] = id
        else:
            context['folderForm'] = FolderForm()
    return render_to_response('folderForm.html',context,context_instance=RequestContext(request))

@login_required
def deleteSermon(request,id=False):
    if id:
        SermonFile.objects.get(pk=id).delete()
        return HttpResponseRedirect(reverse(viewFolder,args=[False]))
    
@login_required
def deleteFolder(request,id=False):
    if id:
        Folder.objects.get(pk=id).delete()
        return HttpResponseRedirect(reverse(viewFolder,args=[False]))
    
@login_required
def editSermon(request,id=False):
    context = {}
    context.update(csrf(request))
    if request.method == 'POST':
        sermonForm = SermonFileForm(request.POST,request.FILES)
        if sermonForm.is_valid() and not id:
            newSermon = sermonForm.save(commit=False)
            newSermon.owner = request.user
            if id:
                newSermon.pk = id
            newSermon.save()
            return HttpResponseRedirect(reverse(viewFolder,args=[False]))
        elif id:
            newSermon = SermonFileForm(request.POST,request.FILES,instance=SermonFile.objects.get(pk=id)).save(commit=False)
            newSermon.owner = request.user
            newSermon.save()
            return HttpResponseRedirect(reverse(viewFolder,args=[False]))
        else:
            context['sermonFileForm'] = sermonForm
            context['error'] = "Correct the errors before submitting"
    elif id:
        context['currID'] = id
        context['sermonFileForm'] = SermonFileForm(instance=SermonFile.objects.get(pk=id))
    else:
        context['sermonFileForm'] = SermonFileForm()
        
    return render_to_response('sermonForm.html',context,context_instance=RequestContext(request))

@login_required
def viewFolder(request,id=False):
    context = {}
    if id:
        thisFolder = Folder.objects.get(pk=id)
        context['fileList'] = SermonFile.objects.filter(fileFolders=thisFolder)
        context['folderList'] = Folder.objects.filter(folder=thisFolder)
        upFolder = Folder.objects.get(pk=id).folder
        if upFolder:
            context['id'] = upFolder.id
        else:
            context['id'] = 0
    else:
        context['fileList'] = SermonFile.objects.filter(fileFolders=None)
        context['folderList'] = Folder.objects.filter(folder=None)
    return render_to_response('folderContents.html',context,context_instance=RequestContext(request))

#@login_required
#def renderPage(request,id=False):
#    context = {}
#    context.update(csrf(request))
#    if id:
#        context['currentFiles'] = SermonFile.objects.filter(fileFolders=Folder.objects.get(pk=id))
#        context['folders'] = Folder.objects.get(folder=Folder.objects.get(pk=id))
#    else:
#        context['currentFiles'] = SermonFile.objects.all()
#        context['folders'] = Folder.objects.all()
#    context['sermonFileForm'] = SermonFileForm()
#    context['blankSermonFileForm'] = SermonFileForm()
#    if request.method == 'POST':
#        sermonForm = SermonFileForm(request.POST,request.FILES)
#        if sermonForm.is_valid():
#            newSermon = sermonForm.save(commit=False)
#            newSermon.owner = request.user
#            newSermon.save()
#            return HttpResponseRedirect(reverse(uploadSermon))
#        else:
#            context['sermonFileForm'] = sermonForm
#            context['error'] = "Correct the errors before submitting"
#    return render_to_response('upload.html',context,context_instance=RequestContext(request))
