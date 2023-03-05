from django.db import models
from accounts.models import Profile

# Create your models here.
class Leave(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    report = models.FileField()
    maternity_leave = models.IntegerField(default=9)
    pregnancy_date = models.DateField()