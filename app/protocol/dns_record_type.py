from enum import IntEnum


class DNSRecordType(IntEnum):
    A = 1  # Host Address
    NS = 2  # Authoritative name server
    MD = 3
    MF = 4
    CNAME = 5  # Canonical name for alias
    SOA = 6  # Start of zone authority
    MB = 7
    MG = 8
    MR = 9
    NULL = 10
    WKS = 11
    PTR = 12
    HINFO = 13
    MINFO = 14
    MX = 15
    TXT = 16  # Text Strings

    def encode(self) -> bytes:
        return int.to_bytes(self, 2, "big")
