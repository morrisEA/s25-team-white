import ndef
import random
import string

class RFIDReader:
    def __init__(self):
        """Initialize the RFID Reader Stub."""
        print("RFID Reader Stub Initialized.")

    def generate_serial_number(self):
        """Generate a random firearm serial number (10 alphanumeric characters)."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def encode_ndef(self, serial_number):
        """Encode a firearm serial number into an NDEF message."""
        ndef_record = ndef.TextRecord(serial_number)
        ndef_message = list(ndef.message_encoder([ndef_record]))
        return ndef_message

    def decode_ndef(self, ndef_message):
        """Decode an NDEF message to extract the firearm serial number."""
        if isinstance(ndef_message, list):
            ndef_message = b"".join(ndef_message)  # Convert list to a single bytes object
        decoded_records = list(ndef.message_decoder(ndef_message))
        for record in decoded_records:
            if isinstance(record, ndef.TextRecord):
                return record.text
        return None

if __name__ == "__main__":
    reader = RFIDReader()
    
    # Generate a serial number
    serial_number = reader.generate_serial_number()
    print("Generated Serial Number:", serial_number)

    # Encode it into NDEF
    encoded_message = reader.encode_ndef(serial_number)
    print("Encoded NDEF Message:", encoded_message)

    # Decode the NDEF message
    decoded_serial = reader.decode_ndef(encoded_message)
    print("Decoded Serial Number:", decoded_serial)
