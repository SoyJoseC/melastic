from socket import fromshare
from django import forms
from melastic.models import Document, MendeleyGroup


class DocumentForm(forms.ModelForm):
    """A class containing the representation of a Document as a form"""
    class Meta:
        model = Document
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            # 'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkform-check'}),
            'doc_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
class EditDocumentForm(forms.ModelForm):
    """A class containing the representation of a Edit Document as a form"""
    class Meta:
        model = Document
        fields = ['tags']

        widgets = {
            #'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            # 'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkform-check'}),
            #'doc_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SelectGroupForm(forms.Form):
    """A class containing the representation of a Selecting Group as a form"""
    
    groups = ['uno', 'dos']
    widgets = {
        'groups': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkform-check'}),
    }



class AddGroupForm(forms.ModelForm):
    """A class containing the representation of Adding a Group as a form"""

    class Meta:
        model = MendeleyGroup
        fields = ['mendeley_username', 'mendeley_password']
        widgets = {
            'mendeley_password': forms.PasswordInput()
        }
