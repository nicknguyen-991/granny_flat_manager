from django.db import models

from accounts.models import Staff
from crm.models import Client


class Project(models.Model):
    """
    One Granny Flat build job.

    Maps to SQL table: projects
    Relationships:
      - many projects -> one client
      - many projects -> one sales staff (optional)
    """

    class Status(models.TextChoices):
        PLANNING = 'planning', 'Planning'
        IN_PROGRESS = 'in_progress', 'In progress'
        COMPLETED = 'completed', 'Completed'
        ON_HOLD = 'on_hold', 'On hold'

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='projects',
        db_column='client_id',
    )
    sales_rep = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        db_column='sales_rep_id',
    )
    contract_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    contract_signed_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']

    def __str__(self):
        return f'Project #{self.pk} — {self.client} [{self.status}]'


class ProjectStage(models.Model):
    """
    Lookup table of standard construction milestones.

    Maps to SQL table: project_stages
    Example rows: site_prep, slab, frame, lockup, fitout, handover
    """

    stage_name = models.CharField(max_length=50, unique=True)
    sequence_order = models.PositiveIntegerField()
    typical_duration_days = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'project_stages'
        ordering = ['sequence_order']

    def __str__(self):
        return f'{self.sequence_order}. {self.stage_name}'


class ProjectStageProgress(models.Model):
    """
    Actual progress of one stage on one project.

    Maps to SQL table: project_stage_progress
    UNIQUE (project, stage) — one progress row per stage per project.
    """

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not started'
        IN_PROGRESS = 'in_progress', 'In progress'
        COMPLETED = 'completed', 'Completed'
        DELAYED = 'delayed', 'Delayed'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='stage_progress',
        db_column='project_id',
    )
    stage = models.ForeignKey(
        ProjectStage,
        on_delete=models.PROTECT,
        related_name='progress_rows',
        db_column='stage_id',
    )
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED,
    )

    class Meta:
        db_table = 'project_stage_progress'
        verbose_name_plural = 'project stage progress'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'stage'],
                name='unique_project_stage',
            ),
        ]

    def __str__(self):
        return f'{self.project_id} / {self.stage} [{self.status}]'


class ProjectUpdate(models.Model):
    """
    Site diary entry (notes / photo URL) for a project.

    Maps to SQL table: project_updates
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='updates',
        db_column='project_id',
    )
    posted_by = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='project_updates',
        db_column='posted_by',
    )
    update_text = models.TextField(blank=True)
    photo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_updates'
        ordering = ['-created_at']

    def __str__(self):
        return f'Update on project {self.project_id} @ {self.created_at:%Y-%m-%d}'
