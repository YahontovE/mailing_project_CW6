from django import forms

from mailing.models import Client, Mailing, MessageMailing

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "valid_ver":
                field.widget.attrs['class'] = 'form-control'
class ClientForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('user',)


class MailingForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ('user','time',)

class MessageForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model=MessageMailing
        fields = '__all__'
        exclude = ('user',)
