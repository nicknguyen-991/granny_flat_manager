from django.db import models

from accounts.models import Staff


class Lead(models.Model):
    """
    Prospective customer before a signed contract.

    Maps to SQL table: leads
    Relationship: many leads can be assigned to one Staff (sales).
    """

    class Source(models.TextChoices):
        GOOGLE_ADS = 'google_ads', 'Google Ads'
        REFERRAL = 'referral', 'Referral'
        WALK_IN = 'walk_in', 'Walk-in'
        WEBSITE = 'website', 'Website'
        ONLINE_STORE = 'online_store', 'Online Store'
        COLD_CALL = 'cold_call', 'Cold Call'
        PUBLIC_RELATIONS = 'public_relations', 'Public Relations'
        SALES_EMAIL_ALIAS = 'sales_email_alias', 'Sales Email Alias'
        SEMINAR_PARTNER = 'seminar_partner', 'Seminar Partner'
        INTERNAL_SEMINAR = 'internal_seminar', 'Internal Seminar'
        TRADE_SHOW = 'trade_show', 'Trade Show'
        WEB_DOWNLOAD = 'web_download', 'Web Download'
        WEB_RESEARCH = 'web_research', 'Web Research'
        CHAT = 'chat', 'Chat'
        X_TWITTER = 'x_twitter', 'X (Twitter)'
        FACEBOOK = 'facebook', 'Facebook'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        CONTACTED = 'contacted', 'Contacted'
        QUOTED = 'quoted', 'Quoted'
        WON = 'won', 'Won'
        LOST = 'lost', 'Lost'

    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    source = models.CharField(
        'Lead Source',
        max_length=30,
        choices=Source.choices,
        null=True,
        blank=True,
    )
    assigned_sales = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
        db_column='assigned_sales_id',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leads'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name} [{self.status}]'


class Client(models.Model):
    """
    Confirmed customer (often converted from a won lead).

    Maps to SQL table: clients
    Relationship: one client can have many projects.
    """

    lead = models.ForeignKey(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients',
        db_column='lead_id',
    )
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    site_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clients'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Commission(models.Model):
    """
    Sales commission linked to a project.

    Maps to SQL table: commissions
    Defined in crm because it is a sales/finance concept.
    Uses string FK to construction.Project to avoid circular imports.
    """

    project = models.ForeignKey(
        'construction.Project',
        on_delete=models.CASCADE,
        related_name='commissions',
        db_column='project_id',
    )
    sales_rep = models.ForeignKey(
        Staff,
        on_delete=models.PROTECT,
        related_name='commissions',
        db_column='sales_rep_id',
    )
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'commissions'
        ordering = ['-id']

    def __str__(self):
        return f'Commission ${self.commission_amount} (project {self.project_id})'
