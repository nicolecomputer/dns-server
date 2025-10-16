from dataclasses import dataclass
from enum import IntEnum

class QueryResponseValue(IntEnum):
    Question = 0
    Reply = 1

@dataclass
class DNSHeader:
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
        data = bytearray()
        data.extend(self.identifier.to_bytes(2, byteorder='big'))

        qr_data = int(self.query_response_indicator)
        opcode_data = int(self.operation_code)
        aa_data = int(self.authoritative_answer)
        tc_data = int(self.truncation)
        rd_data = int(self.recursion_desired)

        byte2 = (qr_data << 7) | (opcode_data << 3) | (aa_data << 2) | (tc_data << 1) | rd_data
        data.append(byte2)

        ra_data = int(self.recursion_available)
        z_data = int(self.reserved)
        rcode_data = int(self.response_code)

        byte3 = (ra_data << 7) | (z_data << 4) | rcode_data
        data.append(byte3)

        data.extend(self.question_count.to_bytes(2, byteorder='big'))
        data.extend(self.answer_count.to_bytes(2, byteorder='big'))
        data.extend(self.authority_record_count.to_bytes(2, byteorder='big'))
        data.extend(self.additional_record_count.to_bytes(2, byteorder='big'))

        return data

    def __str__(self):
        return (
            f"ID: {self.identifier}, QR: {self.query_response_indicator}, OPCODE: {self.operation_code}, AA: {self.authoritative_answer}, "
            f"TC: {self.truncation}, RD: {self.recursion_desired}, RA: {self.recursion_available}, Z: {self.reserved}, RCODE: {self.response_code}, "
            f"QDCOUNT: {self.question_count}, ANCOUNT: {self.answer_count}, NSCOUNT: {self.authority_record_count}, ARCOUNT: {self.additional_record_count}"
        )
