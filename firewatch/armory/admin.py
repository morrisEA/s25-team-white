from django.contrib import admin
from .models import * 
# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "city", "state", "zip_code")
    search_fields = ("city", "state", "zip_code")

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "service_branch", "total_service_members", "location_id")
    search_fields = ("name", "service_branch", "commanding_officer")
    list_filter = ("service_branch",)

@admin.register(ServiceMember)
class ServiceMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "first", "last", "rate", "rank", "end_of_service_date", "command_id")
    search_fields = ("first", "last", "rank", "rate")
    list_filter = ("rank", "command_id")

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ("id", "qual_type", "completion_date", "expiration_date")
    search_fields = ("qual_type",)

@admin.register(Armory)
class ArmoryAdmin(admin.ModelAdmin):
    list_display = ("id", "department", "total_magazines", "command_id")
    search_fields = ("department",)

@admin.register(Armorer)
class ArmorerAdmin(admin.ModelAdmin):
    list_display = ("id", "member_id", "armory_id", "training_exp_date")
    search_fields = ("member_id__first", "member_id__last")

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ("id", "total_m9", "total_m4a1", "total_9mm", "total_556", "total_762", "armory_id")

@admin.register(Firearm)
class FirearmAdmin(admin.ModelAdmin):
    list_display = ("id", "firearm_type", "serial_number", "maintenance_date", "magazine_id")
    search_fields = ("firearm_type", "serial_number")

@admin.register(Ammunition)
class AmmunitionAdmin(admin.ModelAdmin):
    list_display = ("id", "ammunition_type", "lot_number", "firearm_id", "magazine_id")
    search_fields = ("ammunition_type", "lot_number")

@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ("id", "watch_type", "member_id", "check_out", "check_in", "is_qualified", "ammunition_count")
    search_fields = ("watch_type", "member_id__first", "member_id__last")
    list_filter = ("watch_type", "is_qualified", "check_out", "check_in")
    filter_horizontal = ("ammunition_id", "firearm_id", "qualification_id")

