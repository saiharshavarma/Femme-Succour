from django.contrib import admin
from .models import MeetingRecording

# Register your models here.

class MeetingRecordingAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'profile', 'transcript')

admin.site.register(MeetingRecording, MeetingRecordingAdmin)