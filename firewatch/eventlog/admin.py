from django.contrib import admin
from .models import RFIDScan

# Register your models here.
@admin.register(RFIDScan)
class RFIDScanAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'scan_time')
    search_fields = ('serial_number',)
    ordering = ('-scan_time',)