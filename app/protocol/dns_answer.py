from dataclasses import dataclass

from app.protocol.dns_name_field import DNSNameField
from app.protocol.dns_record_class import DNSRecordClass
from app.protocol.dns_record_type import DNSRecordType
from app.protocol.ip_address import IPAddress


@dataclass
class DNSAnswer:
    name: str
    record_type: DNSRecordType
    record_class: DNSRecordClass
    time_to_live: int
    data: IPAddress

    def to_bytes(self) -> bytes:
        encoded_ttl = self.time_to_live.to_bytes(4, byteorder="big")
        encoded_length = self.data.length.to_bytes(2, byteorder="big")

        return (
            DNSNameField(self.name).to_bytes()
            + self.record_type.encode()
            + self.record_class.encode()
            + encoded_ttl
            + encoded_length
            + self.data.encode()
        )
