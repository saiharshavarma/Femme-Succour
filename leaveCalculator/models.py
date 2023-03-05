from django.db import models
from accounts.models import Profile
from django.utils.text import slugify

# Create your models here.
class Leave(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=264, unique=True, default='',editable=False)
    report = models.FileField()
    maternity_leave = models.IntegerField(default=9)
    pregnancy_date = models.DateField()
    leave_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.profile) + str(self.timestamp), allow_unicode=True)
        super().save(*args, **kwargs)