from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class SermonFile(models.Model):
    name = models.CharField(max_length=100,blank=True)
    dateUploaded = models.DateTimeField(auto_now_add=True)
    sermonDate = models.DateField(default=datetime.now)
    audioFile = models.FileField(upload_to='sermons/')
    owner = models.ForeignKey(User)
    downloadNumber = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

    def clean(self):
        self.name = self.audioFile.name

class Iptracker(models.Model):
    sermonFile = models.ForeignKey(SermonFile)
    ip = models.IPAddressField()
    dateClicked = models.DateTimeField(auto_now_add=True)
    
class Folder(models.Model):
    name = models.CharField(max_length=100)
    files = models.ManyToManyField(SermonFile,related_name='fileFolders',blank=True,null=True,default=None)
    folder = models.ForeignKey('Folder',null=True,blank=True,default=None,related_name='containingFolder')
    def __unicode__(self):
        return self.name
