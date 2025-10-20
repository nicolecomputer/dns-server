from dataclasses import dataclass
from enum import IntEnum
import bitstruct # type: ignore

class QueryResponseValue(IntEnum):
    Question = 0
    Reply = 1

@dataclass
class DNSHeader:
    """
    DNS Header Format:
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|Z|AD|CD|    RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """

    identifier: int # 16 bits

    query_response_indicator: QueryResponseValue # 1 bit
    operation_code: int # 4 bits (probably an enum later)
    authoritative_answer: bool # 1 bit
    truncation: bool # 1 bit
    recursion_desired: bool # 1 bit
    recursion_available: bool #1 bit
    reserved: int #3 bits
    response_code: int # 4 bits (probably an enum later)

    question_count: int # 16 bits

    answer_count: int # 16 bits

    authority_record_count: int # 16 bits

    additional_record_count: int # 16 bits

    def to_bytes(self):
        qr = int(self.query_response_indicator)
        opcode = int(self.operation_code)
        aa = int(self.authoritative_answer)
        tc = int(self.truncation)
        rd = int(self.recursion_desired)
        ra = int(self.recursion_available)
        z = int(self.reserved)
        rcode = int(self.response_code)

        data = bitstruct.pack(
            'u16u1u4u1u1u1u1u3u4u16u16u16u16',
            self.identifier,
            qr, opcode, aa, tc, rd, ra, z, rcode,
            self.question_count,
            self.answer_count,
            self.authority_record_count,
            self.additional_record_count)

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> 'DNSHeader':
        unpacked = bitstruct.unpack(
            'u16u1u4u1u1u1u1u3u4u16u16u16u16',
            data[:12]
        )

        # Destructure the tuple
        (identifier, qr, opcode, aa, tc, rd, ra, z, rcode,
        qdcount, ancount, nscount, arcount) = unpacked

        return DNSHeader(
            identifier=identifier,
            query_response_indicator=QueryResponseValue(qr),
            operation_code=opcode,
            authoritative_answer=bool(aa),
            truncation=bool(tc),
            recursion_desired=bool(rd),
            recursion_available=bool(ra),
            reserved=z,
            response_code=rcode,
            question_count=qdcount,
            answer_count=ancount,
            authority_record_count=nscount,
            additional_record_count=arcount
        )

    def __str__(self):
        return (
            f"ID: {self.identifier}, QR: {self.query_response_indicator}, OPCODE: {self.operation_code}, AA: {self.authoritative_answer}, "
            f"TC: {self.truncation}, RD: {self.recursion_desired}, RA: {self.recursion_available}, Z: {self.reserved}, RCODE: {self.response_code}, "
            f"QDCOUNT: {self.question_count}, ANCOUNT: {self.answer_count}, NSCOUNT: {self.authority_record_count}, ARCOUNT: {self.additional_record_count}"
        )
