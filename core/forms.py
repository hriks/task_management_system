from django import forms
from core.models import Operator


class OperatorForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    def save(self, commit=True):
        password = self.cleaned_data.get('password', None)
        return super(OperatorForm, self).save(commit=commit)

    class Meta:
        model = Operator
        fields = '__all__'
