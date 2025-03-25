from django.db import transaction
from authentication.models import MilitaryPersonnel, Firearm, FirearmTransaction
from django.contrib.auth import authenticate
from authentication.connectors.base_connector import BaseDatabaseConnector

class SQLORMDatabaseConnector(BaseDatabaseConnector):
    """Django ORM Database Connector"""

    def save_personnel(self, personnel_data):
        """Saves military personnel in SQL database"""
        with transaction.atomic():
            personnel = MilitaryPersonnel.objects.create(**personnel_data)
            personnel.set_password(personnel_data["password"])  
            personnel.save()

    def authenticate_personnel(self, username, password):
        """Uses Django's built-in authentication system"""
        return authenticate(username=username, password=password)

    def save_firearm(self, firearm_data):
        """Saves firearm record in SQL database"""
        with transaction.atomic():
            Firearm.objects.create(**firearm_data)

    def check_out_firearm(self, firearm_id, personnel_id):
        """Assign a firearm to a military personnel"""
        with transaction.atomic():
            personnel = MilitaryPersonnel.objects.get(id=personnel_id)
            firearm = Firearm.objects.get(id=firearm_id)
            FirearmTransaction.objects.create(firearm=firearm, personnel=personnel, status="OUT")
