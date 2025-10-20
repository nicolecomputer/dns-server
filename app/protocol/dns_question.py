from dataclasses import dataclass
from enum import IntEnum

NULL_BYTE = b'\x00'

def encode_label(label: str) -> bytes:
    encoded = label.encode("ascii")
    encoded_len = bytes([len(encoded)])

    return encoded_len + encoded

@dataclass
class DNSQuestionName:
    name: str

    def to_bytes(self) -> bytes:
        if not self.name:
            return NULL_BYTE

        labels = self.name.split(".")
        encoded_labels = [encode_label(label) for label in labels]

        return b''.join(encoded_labels) + NULL_BYTE


class DNSQuestionType(IntEnum):
    A = 1 # Host Address
    NS = 2 # Authoritative name server
    MD = 3
    MF = 4
    CNAME = 5 # Canonical name for alias
    SOA = 6 # Start of zone authority
    MB = 7
    MG = 8
    MR = 9
    NULL = 10
    WKS = 11
    PTR = 12
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16 # Text Strings

    def encode(self) -> bytes:
        return int.to_bytes(self, 2, 'big')

class DNSQuestionClass(IntEnum):
    IN = 1 # The internet

    def encode(self) -> bytes:
        return int.to_bytes(self, 2, 'big')

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
    question_type: DNSQuestionType
    question_class: DNSQuestionClass

    def to_bytes(self) -> bytes:
        return DNSQuestionName(self.name).to_bytes() + \
                self.question_type.encode() + \
                self.question_class.encode()
