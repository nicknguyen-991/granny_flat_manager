from django.contrib import admin

from .models import Project, ProjectStage, ProjectStageProgress, ProjectUpdate


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'sales_rep',
        'status',
        'contract_value',
        'contract_signed_date',
        'created_at',
    )
    list_filter = ('status',)
    search_fields = ('client__first_name', 'client__last_name')


@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('sequence_order', 'stage_name', 'typical_duration_days')
    ordering = ('sequence_order',)


@admin.register(ProjectStageProgress)
class ProjectStageProgressAdmin(admin.ModelAdmin):
    list_display = (
        'project',
        'stage',
        'status',
        'planned_start_date',
        'planned_end_date',
        'actual_start_date',
        'actual_end_date',
    )
    list_filter = ('status',)


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('project', 'posted_by', 'created_at')
    search_fields = ('update_text',)
