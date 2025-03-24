"""
forms.py - Handles RFID Scan Form Generation

This file defines a Django form used to simulate an RFID scan. 
It automatically generates a random firearm serial number in the
standard Fire Watch format (e.g., FW-123456), and makes the field
read-only to mimic how a real RFID scanner would provide input.

This form is tied to the RFIDScan model and is used in the frontend
as part of the modal to simulate scanning behavior.
""" 

from django import forms
from .models import RFIDScan
import random
import string

class RFIDScanForm(forms.ModelForm):
    class Meta:
        model = RFIDScan
        fields = ['serial_number']
        # Make the field read-only to simulate RFID input (not editable by user)
        widgets = {
            'serial_number': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(RFIDScanForm, self).__init__(*args, **kwargs)
        # Automatically generate a random serial number when the form is initialized
        self.fields['serial_number'].initial = self.generate_serial_number()

    def generate_serial_number(self):
        # Fire Watch standard format: FW-XXXXXX (X = digit)
        prefix = "FW"
        digits = ''.join(random.choices(string.digits, k=6))
        return f"{prefix}-{digits}"
