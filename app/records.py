from dataclasses import dataclass
from typing import Optional
from app.protocol.dns_answer import DNSAnswer
from app.protocol.dns_record_class import DNSRecordClass
from app.protocol.dns_record_type import DNSRecordType
from app.protocol.ip_address import IPAddress


@dataclass
class DNSRecord:
    name: str
    record_type: DNSRecordType
    time_to_live: int
    data: IPAddress

    def to_dns_answer(self) -> DNSAnswer:
        return DNSAnswer(
            name=self.name,
            record_class=DNSRecordClass.IN,
            record_type=self.record_type,
            time_to_live=self.time_to_live,
            data=self.data,
        )


def find_records(
    records: list[DNSRecord],
    name: str,
    record_type: Optional[DNSRecordType] = None,
) -> list[DNSRecord]:
    found: list[DNSRecord] = []

    for record in records:
        isValid = record.name == name

        if (record_type is not None and record.record_type != record_type):
            isValid = False

        if isValid:
            found.append(record)

    return found

