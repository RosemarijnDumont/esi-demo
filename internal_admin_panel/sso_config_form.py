from django import forms
from ..models import SSOConfiguration

class SSOConfigurationForm(forms.ModelForm):
    class Meta:
        model = SSOConfiguration
        fields = ['sso_enabled', 'idp_metadata_url', 'entity_id', 'acs_url', 'x509cert']
        widgets = {
            'idp_metadata_url': forms.URLInput(attrs={'class': 'form-control'}),
            'entity_id': forms.TextInput(attrs={'class': 'form-control'}),
            'acs_url': forms.URLInput(attrs={'class': 'form-control'}),
            'x509cert': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'sso_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }