from django.db import models

class RFIDScan(models.Model):
	"""Model to store RFID scan data."""
	serial_number = models.CharField(max_length=20, unique=True)
	scan_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.serial_number} - {self.scan_time}"
