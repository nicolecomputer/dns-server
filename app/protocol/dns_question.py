from dataclasses import dataclass

from app.protocol.dns_name_field import DNSNameField
from app.protocol.dns_record_class import DNSRecordClass
from app.protocol.dns_record_type import DNSRecordType


@dataclass
class DNSQuestion:
    """
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """

    name: str
    record_type: DNSRecordType
    record_class: DNSRecordClass

    def to_bytes(self) -> bytes:
        return (
            DNSNameField(self.name).to_bytes()
            + self.record_type.encode()
            + self.record_class.encode()
        )
