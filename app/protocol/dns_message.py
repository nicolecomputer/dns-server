from dataclasses import dataclass

from app.protocol.dns_answer import DNSAnswer
from app.protocol.dns_header import DNSHeader
from app.protocol.dns_question import DNSQuestion, DNSRecordClass
from app.protocol.dns_record_type import DNSRecordType

POINTER_FLAG = 0xC0  # Binary: 11000000
OFFSET_MASK = 0x3FFF  # Binary: 00111111 11111111
POINTER_BYTE_LENGTH = 2


def parse_header(starting_position: int, data: bytes) -> tuple[DNSHeader, int]:
    header_length = 12
    return DNSHeader.from_bytes(data[starting_position:header_length]), header_length


def parse_domain_name(data: bytes, start_offset: int) -> tuple[list[str], int]:
    name_parts = []
    offset = start_offset

    while True:
        next_byte = data[offset]

        # Compression (ugh) so this gets handled specially
        # https://www.rfc-editor.org/rfc/rfc1035#section-4.1.4
        if next_byte & POINTER_FLAG == POINTER_FLAG:
            pointer_offset = (
                int.from_bytes(data[offset : offset + POINTER_BYTE_LENGTH], "big")
                & OFFSET_MASK
            )

            part_at_pointer, _ = parse_domain_name(data, pointer_offset)
            name_parts.extend(part_at_pointer)
            offset += POINTER_BYTE_LENGTH
            break

        # This is the end byte so we consume it and move on
        if next_byte == 0:
            offset += 1
            break

        # The normal case, we read the data
        length = next_byte
        offset += 1  # We read the length and have consumed that byte
        label = data[offset : offset + length].decode("ascii")
        name_parts.append(label)
        offset += length

    return name_parts, offset - start_offset


def parse_questions(
    header: DNSHeader, starting_position: int, data: bytes
) -> tuple[list[DNSQuestion], int]:
    questions: list[DNSQuestion] = []
    offset = starting_position

    for _ in range(header.question_count):
        name_parts, bytes_consumed = parse_domain_name(data, offset)
        offset += bytes_consumed
        name = ".".join(name_parts)

        #  QTYPE (2 bytes)
        qtype = int.from_bytes(data[offset : offset + 2], "big")
        offset += 2

        #  QCLASS (2 bytes)
        qclass = int.from_bytes(data[offset : offset + 2], "big")
        offset += 2

        question = DNSQuestion(
            name=name,
            record_type=DNSRecordType(qtype),
            record_class=DNSRecordClass(qclass),
        )
        questions.append(question)

    return questions, offset - starting_position  # Return bytes consumed


@dataclass
class DNSMessage:
    header: DNSHeader
    questions: list[DNSQuestion]
    answers: list[DNSAnswer]

    def to_bytes(self) -> bytes:
        result = b""

        result += self.header.to_bytes()

        for question in self.questions:
            result += question.to_bytes()

        for answer in self.answers:
            result += answer.to_bytes()

        return result

    @classmethod
    def from_bytes(cls, data: bytes) -> "DNSMessage":
        byte_offset = 0

        header, bytes_consumed = parse_header(byte_offset, data)
        byte_offset += bytes_consumed

        questions, bytes_consumed = parse_questions(header, byte_offset, data)
        byte_offset += bytes_consumed

        return DNSMessage(header=header, questions=questions, answers=[])
