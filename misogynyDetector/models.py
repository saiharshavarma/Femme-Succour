from django.db import models
from accounts.models import Profile

# Create your models here.
class MeetingRecording(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    recording = models.FileField()
    transcript = models.TextField()