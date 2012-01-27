from django.forms import ModelForm
from churchWeb.sermons.models import  SermonFile, Folder

class SermonFileForm(ModelForm):
    class Meta:
        model = SermonFile
        exclude = ['owner','downloadNumber']
        
class FolderForm(ModelForm):
    class Meta:
        model = Folder