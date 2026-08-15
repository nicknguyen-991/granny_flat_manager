from django import forms

from partners.models import Partner, ProjectPartner

from .models import Project, ProjectStageProgress, ProjectUpdate


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'client',
            'sales_rep',
            'contract_value',
            'contract_signed_date',
            'status',
        ]
        widgets = {
            'contract_signed_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StageProgressForm(forms.ModelForm):
    class Meta:
        model = ProjectStageProgress
        fields = [
            'status',
            'planned_start_date',
            'planned_end_date',
            'actual_start_date',
            'actual_end_date',
        ]
        widgets = {
            'planned_start_date': forms.DateInput(attrs={'type': 'date'}),
            'planned_end_date': forms.DateInput(attrs={'type': 'date'}),
            'actual_start_date': forms.DateInput(attrs={'type': 'date'}),
            'actual_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ProjectPartnerForm(forms.ModelForm):
    class Meta:
        model = ProjectPartner
        fields = ['partner', 'trade_role', 'agreed_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['partner'].queryset = Partner.objects.filter(active=True)


class ProjectUpdateForm(forms.ModelForm):
    class Meta:
        model = ProjectUpdate
        fields = ['posted_by', 'update_text', 'photo_url']
        widgets = {
            'update_text': forms.Textarea(attrs={'rows': 3}),
        }
