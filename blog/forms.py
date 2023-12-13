from blog.models import BlogEntry
from django import forms


class EntryForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False)

    class Meta:
        model = BlogEntry
        fields = ("entry_title", "entry_body", "entry_img", "is_published")

        widgets = {
            "entry_title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок'
            }),
            "entry_body": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Содержание записи'
            }),
            "entry_img": forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Картинка'
            }),

        }
