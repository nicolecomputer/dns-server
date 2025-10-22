from dataclasses import dataclass

from app.protocol.dns_answer import DNSAnswer
from app.protocol.dns_question import DNSQuestion
from app.protocol.ip_address import IPAddress


@dataclass
class DNSServer:
    address: IPAddress
    port: int


def request_dns_record_from(
    server: DNSServer, question: DNSQuestion
) -> list[DNSAnswer]:
    raise NotImplementedError()
