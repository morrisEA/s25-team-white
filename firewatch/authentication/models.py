from django.db import models
from django.contrib.auth.models import AbstractUser

class MilitaryPersonnel(AbstractUser):
    """Custom Military Personnel model for authentication"""
    rank = models.CharField(max_length=50)
    unit = models.CharField(max_length=100)


    groups = models.ManyToManyField(
        "auth.Group",
        related_name="military_personnel_set",  # Custom related_name to prevent conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="military_personnel_permissions_set",  # Custom related_name to prevent conflict
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.rank} - {self.unit}"


class FirearmTransaction(models.Model):
    """Tracks firearm checkouts and check-ins"""
    personnel = models.ForeignKey(MilitaryPersonnel, on_delete=models.CASCADE)
    firearm_id = models.CharField(max_length=64)  
    status = models.CharField(max_length=10, choices=[("OUT", "Checked Out"), ("IN", "Checked In")])
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.personnel.username} - {self.firearm_id} - {self.status}"
