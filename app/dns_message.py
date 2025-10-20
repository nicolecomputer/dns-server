from dataclasses import dataclass
from dns_header import DNSHeader
from dns_question import DNSQuestion

@dataclass
class DNSMessage:
    header: DNSHeader
    questions: list[DNSQuestion]

    def to_bytes(self) -> bytes:
        result = b''

        result += self.header.to_bytes()

        for question in self.questions:
            result += question.to_bytes()

        return result

