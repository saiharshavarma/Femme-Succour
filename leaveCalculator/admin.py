from django.contrib import admin
from .models import Leave

# Register your models here.

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'profile', 'maternity_leave')

admin.site.register(Leave, LeaveAdmin)