from django import forms
from core.models import Operator


class OperatorForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    def save(self, commit=True):
        password = self.cleaned_data.get('password', None)
        super(OperatorForm, self).save(commit=commit)
        from core.models import Vault
        Vault.create(self.instance.id, password)
        return self.instance

    class Meta:
        model = Operator
        fields = '__all__'
