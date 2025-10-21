from dataclasses import dataclass
from app.protocol.dns_header import DNSHeader
from app.protocol.dns_question import DNSQuestion, DNSRecordClass
from app.protocol.dns_record_type import DNSRecordType
from app.protocol.dns_answer import DNSAnswer

def parse_header(starting_position: int, data: bytes) -> tuple[DNSHeader, int]:
    header_length = 12
    return DNSHeader.from_bytes(data[starting_position:header_length]), header_length


def parse_questions(header: DNSHeader, starting_position: int, data: bytes) -> tuple[list[DNSQuestion], int]:
    questions: list[DNSQuestion] = []
    offset = starting_position

    for _ in range(header.question_count):
        # Parse QNAME
        name_parts = []
        while True:
            length = data[offset]
            offset += 1

            if length == 0:
                break

            label = data[offset:offset + length].decode('ascii')
            name_parts.append(label)
            offset += length

        name = '.'.join(name_parts)

        #  QTYPE (2 bytes)
        qtype = int.from_bytes(data[offset:offset + 2], 'big')
        offset += 2

        #  QCLASS (2 bytes)
        qclass = int.from_bytes(data[offset:offset + 2], 'big')
        offset += 2

        question = DNSQuestion(
            name=name,
            record_type=DNSRecordType(qtype),
            record_class=DNSRecordClass(qclass)
        )
        questions.append(question)

    return questions, offset - starting_position  # Return bytes consumed
@dataclass
class DNSMessage:
    header: DNSHeader
    questions: list[DNSQuestion]
    answers: list[DNSAnswer]

    def to_bytes(self) -> bytes:
        result = b''

        result += self.header.to_bytes()

        for question in self.questions:
            result += question.to_bytes()

        for answer in self.answers:
            result += answer.to_bytes()

        return result

    @classmethod
    def from_bytes(cls, data: bytes) -> 'DNSMessage':
        byte_offset = 0

        header, bytes_consumed = parse_header(byte_offset, data)
        byte_offset += bytes_consumed

        questions, bytes_consumed = parse_questions(header, byte_offset, data)
        byte_offset += bytes_consumed

        return DNSMessage(
            header=header,
            questions=questions,
            answers=[]
        )

