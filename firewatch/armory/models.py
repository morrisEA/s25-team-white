from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User


# Create your models here.
class Location(models.Model):
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=32)
    zip_code = models.IntegerField()

    def __str__(self):
        return f"{self.city}, {self.state}, {self.zip_code}"


class Command(models.Model):
    name = models.CharField(max_length=64)
    service_branch = CharField(max_length=32)
    total_service_members = models.IntegerField()
    commanding_officer = CharField(max_length=64)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.service_branch}, {self.total_service_members}, {self.commanding_officer}"


class ServiceMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="servicemember", null=True, blank=True)
    first = models.CharField(max_length=32)
    last = models.CharField(max_length=32)
    rate = models.CharField(max_length=8)
    rank = models.CharField(max_length=8)
    end_of_service_date = models.DateField()
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last}, {self.first}"

class Qualification(models.Model):
    qual_type = models.CharField(max_length=64)
    completion_date = models.DateField()
    expiration_date = models.DateField()
    servicemember_id = models.ForeignKey(ServiceMember, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.qual_type}, cmp:{self.completion_date}, exp:{self.expiration_date}"

class Armory(models.Model):
    department = models.CharField(max_length=64)
    total_magazines = models.IntegerField()
    command_id = models.ForeignKey(Command, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department}, mag_total:{self.total_magazines}"

class Armorer(models.Model):
    training_exp_date = models.DateField()
    member_id = models.ForeignKey(ServiceMember, on_delete=models.CASCADE)
    armory_id = models.ForeignKey(Armory, on_delete=models.CASCADE)

    def __str__(self):
        return f"member:{self.member_id}, exp:{self.training_exp_date}"

class Magazine(models.Model):
    total_m9 = models.IntegerField()
    total_m4a1 = models.IntegerField()
    total_9mm = models.IntegerField()
    total_556 = models.IntegerField()
    total_762 = models.IntegerField()
    armory_id = models.ForeignKey(Armory, on_delete=models.CASCADE)

    def __str__(self):
        return f"m9:{self.total_m9}, m4a1:{self.total_m4a1}, 9mm:{self.total_9mm}, 5.56:{self.total_556}, 7.62:{self.total_762}, id:{self.armory_id}"

class Firearm(models.Model):
    firearm_type = models.CharField(max_length=64)
    serial_number = models.CharField(max_length=64)
    maintenance_date = models.DateField()
    available = models.BooleanField(default=True)
    magazine_id = models.ForeignKey(Magazine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firearm_type}, sn:{self.serial_number}, {self.maintenance_date}"


class Ammunition(models.Model):
    ammunition_type = models.CharField(max_length=64)
    lot_number = models.CharField(max_length=64)
    firearm_id = models.ForeignKey(Firearm, on_delete=models.CASCADE)
    magazine_id = models.ForeignKey(Magazine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ammunition_type}, ln:{self.lot_number}"
    
class WatchType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Watch(models.Model):
    watch_type = models.ForeignKey(WatchType, on_delete=models.CASCADE)
    is_qualified = models.BooleanField()
    check_out = models.DateTimeField()
    check_in = models.DateTimeField()
    ammunition_count = models.IntegerField()
    ammunition_id = models.ManyToManyField(Ammunition)
    firearm_id = models.ManyToManyField(Firearm)
    armory_id = models.ForeignKey(Armorer, on_delete=models.CASCADE)
    member_id = models.ForeignKey(ServiceMember, on_delete=models.CASCADE)
    qualification_id = models.ManyToManyField(Qualification)

    def __str__(self):
        return f"Watch: {self.watch_type}, Member: {self.member_id.first} {self.member_id.last}, Check-Out: {self.check_out}, Check-In: {self.check_in}, Qualified: {self.is_qualified}"
