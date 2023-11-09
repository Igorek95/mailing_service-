from django import forms
from .models import Message

class MailingForm(forms.ModelForm):
    pass



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body', 'mailing']
