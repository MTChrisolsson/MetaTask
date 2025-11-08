from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Organization

class StationConfiguration(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='station_configurations'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    default_status = models.CharField(max_length=100, default="pending")
    allowed_statuses = models.JSONField(default=list)
    required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        unique_together = ['organization', 'name']

    def __str__(self):
        return f"{self.organization.name} - {self.name}"

    def clean(self):
        if not isinstance(self.allowed_statuses, list):
            raise ValidationError({
                'allowed_statuses': 'Must be a list of status strings'
            })
        
        if self.default_status not in self.allowed_statuses:
            raise ValidationError({
                'default_status': 'Must be one of the allowed statuses'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)