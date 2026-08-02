from django.db import models


class Partner(models.Model):
    """
    Trade partner / subcontractor in the network.

    Maps to SQL table: partners
    Relationship: many-to-many with Project via ProjectPartner.
    """

    company_name = models.CharField(max_length=150)
    abn = models.CharField(max_length=20, blank=True)
    contact_name = models.CharField(max_length=150, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(max_length=150, blank=True)
    trade_type = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. builder, electrician, plumber, concreter",
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'partners'
        ordering = ['company_name']

    def __str__(self):
        return self.company_name


class ProjectPartner(models.Model):
    """
    Junction table: assigns a partner to a project for a trade role.

    Maps to SQL table: project_partners
    Cardinality: projects * ----<>---- * partners
    """

    project = models.ForeignKey(
        'construction.Project',
        on_delete=models.CASCADE,
        related_name='project_partners',
        db_column='project_id',
    )
    partner = models.ForeignKey(
        Partner,
        on_delete=models.PROTECT,
        related_name='project_partners',
        db_column='partner_id',
    )
    trade_role = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. concreting, framing, electrical",
    )
    agreed_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'project_partners'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'partner', 'trade_role'],
                name='unique_project_partner_trade_role',
            ),
        ]

    def __str__(self):
        role = self.trade_role or 'general'
        return f'{self.partner} on project {self.project_id} ({role})'
