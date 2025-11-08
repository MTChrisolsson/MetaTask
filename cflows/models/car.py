from django.db import models
from django.utils import timezone
from accounts.models import Organization
from datetime import datetime
from ..utils import car_file_path

def get_default_station_fields():
    """
    Returns default station fields based on organization's configuration.
    This will be populated when a car is created with the organization's
    specific station configuration.
    """
    return {}

class Car(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='cars'
    )
    make = models.CharField(max_length=100, default="")
    model = models.CharField(max_length=100, default="")
    registration_number = models.CharField(max_length=6, unique=True, null=True, blank=True)
    color = models.CharField(max_length=50, default="Not specified")
    year = models.PositiveIntegerField(null=True, blank=True)
    mileage = models.PositiveIntegerField(null=True, blank=True)
    files = models.FileField(upload_to=car_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    station_fields = models.JSONField(
        default=get_default_station_fields,
        blank=True,
        help_text="Custom station fields for the car."
    )
    metadata = models.JSONField(default=dict, blank=True)
    tags = models.JSONField(default=list, blank=True)
    notes = models.JSONField(default=list, blank=True)
    messages = models.JSONField(default=list, blank=True)
    custom_car_info = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.registration_number})"

    def clean(self):
        """
        Validate station fields against organization's configuration
        """
        from django.core.exceptions import ValidationError
        
        if self.organization:
            station_configs = {
                sc.name.lower(): sc 
                for sc in self.organization.station_configurations.all()
            }
            
            for station_name, data in self.station_fields.items():
                if station_name not in station_configs:
                    raise ValidationError({
                        'station_fields': f'Station "{station_name}" is not configured for this organization'
                    })
                    
                config = station_configs[station_name]
                if isinstance(data, dict) and 'status' in data:
                    if data['status'] not in config.allowed_statuses:
                        raise ValidationError({
                            'station_fields': f'Status "{data["status"]}" is not allowed for station "{station_name}"'
                        })

        super().clean()

    def save(self, *args, **kwargs):
        if not self.pk and self.organization:  # New car being created
            # Initialize station fields from organization's configuration
            for config in self.organization.station_configurations.all():
                station_name = config.name.lower()
                if station_name not in self.station_fields:
                    self.station_fields[station_name] = {
                        "status": config.default_status,
                        "timestamp": None,
                        "history": []
                    }
        
        self.full_clean()
        super().save(*args, **kwargs)