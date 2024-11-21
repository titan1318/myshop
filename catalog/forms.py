from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Version

class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

class VersionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current']

class FeedbackForm(forms.Form, StyledFormMixin):
    name = forms.CharField(label='Ваше имя', max_length=100)
    email = forms.EmailField(label='Ваш Email')
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'available', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        for word in self.forbidden_words:
            if word.lower() in name.lower():
                raise ValidationError(f'Название содержит запрещенное слово: "{word}"')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        for word in self.forbidden_words:
            if word.lower() in description.lower():
                raise ValidationError(f'Описание содержит запрещенное слово: "{word}"')
        return description
