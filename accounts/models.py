from django.db import models


class Staff(models.Model):
    """
    Internal staff member (admin, sales, site manager).

    Maps to SQL table: users
    We name the model Staff so it does not clash with Django's built-in auth User.
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        SALES = 'sales', 'Sales'
        SITE_MANAGER = 'site_manager', 'Site manager'

    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        ordering = ['last_name', 'first_name']
        verbose_name = 'staff member'
        verbose_name_plural = 'staff members'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role})'
