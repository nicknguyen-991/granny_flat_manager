from django import forms

from .models import Client, Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'first_name',
            'last_name',
            'phone',
            'mobile',
            'email',
            'source',
            'assigned_sales',
            'status',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'lead',
            'first_name',
            'last_name',
            'phone',
            'mobile',
            'email',
            'site_address',
        ]
        widgets = {
            'site_address': forms.Textarea(attrs={'rows': 3}),
        }


class ConvertToClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['site_address']
        widgets = {
            'site_address': forms.Textarea(attrs={'rows': 3}),
        }
