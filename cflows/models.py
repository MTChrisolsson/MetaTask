from django.db import models

from accounts.models import Organization 

class Car(models.Model):
    # Key to know what org the user is connected to
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,  # If org is deleted, remove the cars.
        verbose_name="Owning Organization"
    )
    
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    # ... resten av dina Car-fält ...

    def __str__(self):
        return f"{self.make} ({self.organization.name})"