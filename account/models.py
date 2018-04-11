from django.db import models
from django.contrib.auth.models import User
from dashboard.models import TaxOffice

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(TaxOffice, related_name='tax_office', blank=True,null=True,on_delete=models.CASCADE)
    # audit params
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)