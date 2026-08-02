from django.contrib import admin

from .models import Partner, ProjectPartner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'trade_type',
        'contact_name',
        'contact_phone',
        'active',
    )
    list_filter = ('active', 'trade_type')
    search_fields = ('company_name', 'abn', 'contact_name')


@admin.register(ProjectPartner)
class ProjectPartnerAdmin(admin.ModelAdmin):
    list_display = ('project', 'partner', 'trade_role', 'agreed_price')
    search_fields = ('partner__company_name', 'trade_role')
