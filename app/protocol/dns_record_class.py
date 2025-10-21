from enum import IntEnum

class DNSRecordClass(IntEnum):
    IN = 1 # The internet

    def encode(self) -> bytes:
        return int.to_bytes(self, 2, 'big')
