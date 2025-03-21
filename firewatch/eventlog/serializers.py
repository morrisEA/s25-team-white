from rest_framework import serializers
from .models import RFIDScan

class RFIDScanSerializer(serializers.ModelSerializer):
	"""Serializer for converting RFIDScan model instances to JSON and vice versa."""
	class Meta:
		model = RFIDScan
		fields = ['id', 'serial_number', 'scan_time']