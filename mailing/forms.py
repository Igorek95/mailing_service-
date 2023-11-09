from django import forms
from .models import Message, Mailing


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['send_time', 'frequency', 'status']

        widgets = {
            'send_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'send_time': 'Время отправки',
            'frequency': 'Частота отправки',
            'status': 'Статус',
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body', 'mailing']
