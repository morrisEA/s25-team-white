import time
import random
import uuid

class RFIDReader:
	def __init__(self):
		"""Initialize a simulated RFID reader with an empty scan log"""
		self.scan_log = []

	def generate_fake_scan(self):
		"""Simulate an RFID scan event with a random tag ID and timestamp."""
		tag_id = str(uuid.uuid4())[:8] # generate short unique tag ID
		timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

		scan_event = {
			"tag_id": tag_id,
			"timestamp": timestamp
		}

		self.scan_log.append(scan_event) # store the scan event in memory
		return scan_event

	def simulate_scanning(self, num_scans=5, delay=2):
		"""Simulate multiple scans with a delay between them."""
		print(f"Starting RFID scan simulation for {num_scans} scans...")
		for _ in range(num_scans):
			scan = self.generate_fake_scan()
			print(f"Scanned: {scan}")
			time.sleep(delay) 	# simulate delay between scans

	def get_scan_log(self):
		"""Return the list of all simulated scan events."""
		return self.scan_log

# If running this file directly, test the RFID simulation
if __name__ == "__main__":
	reader = RFIDReader()
	reader.simulate_scanning()