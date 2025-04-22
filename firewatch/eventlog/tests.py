from django.test import TestCase
from django.urls import reverse
from armory.models import Firearm, Magazine
from .forms import RFIDScanForm
import datetime

class RFIDScanEntryViewTest(TestCase):
    def setUp(self):
        self.magazine = Magazine.objects.create(total_m9=10, total_m4a1=20, total_9mm=30, total_556=40, total_762=50, armory_id=None)
        self.serial_number = "1234567890"
        Firearm.objects.create(
            firearm_type="M9",
            serial_number=self.serial_number,
            maintenance_date=datetime.datetime.now(),
            available=True,
            magazine_id=self.magazine
        )

    def test_rfid_scan_entry_post_new_firearm(self):
        data = {
            'serial_number': '9876543210', 
            'firearm_type': 'M4A1',
            'magazine': self.magazine.id
        }

        response = self.client.post(reverse('eventlog:rfid_scan_entry'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Firearm 9876543210 added to inventory.")
        self.assertTemplateUsed(response, 'eventlog/rfid_scan_entry.html')

        self.assertTrue(Firearm.objects.filter(serial_number='9876543210').exists())

    def test_rfid_scan_entry_post_existing_firearm(self):
        data = {
            'serial_number': self.serial_number,  
            'firearm_type': 'M240B',
            'magazine': self.magazine.id
        }

        response = self.client.post(reverse('eventlog:rfid_scan_entry'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"A firearm with serial number '{self.serial_number}' already exists.")
        self.assertTemplateUsed(response, 'eventlog/rfid_scan_entry.html')
