from django.contrib import admin

from .models import Client, Commission, Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'phone',
        'mobile',
        'status',
        'source',
        'assigned_sales',
        'created_at',
    )
    list_filter = ('status', 'source')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'mobile')
    fields = (
        'first_name',
        'last_name',
        'phone',
        'mobile',
        'email',
        'source',
        'assigned_sales',
        'status',
        'notes',
        'created_at',
    )
    readonly_fields = ('created_at',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'phone',
        'mobile',
        'email',
        'lead',
        'created_at',
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'mobile', 'site_address')
    fields = (
        'lead',
        'first_name',
        'last_name',
        'phone',
        'mobile',
        'email',
        'site_address',
        'created_at',
    )
    readonly_fields = ('created_at',)


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('project', 'sales_rep', 'commission_amount', 'paid', 'paid_date')
    list_filter = ('paid',)
