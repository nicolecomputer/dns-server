from app.protocol.dns_message import DNSMessage
from app.protocol.dns_header import DNSHeader, QueryResponseValue
from app.protocol.dns_answer import DNSAnswer
from app.protocol.dns_record_class  import DNSRecordClass
from app.protocol.dns_record_type import DNSRecordType
from app.protocol.ip_address import IPAddress

DNSRequest = DNSMessage
DNSResponse = DNSMessage


def handle_dns_query(request: DNSRequest) -> DNSResponse:
    return DNSResponse(
        header=DNSHeader(
            identifier=request.header.identifier,
            query_response_indicator=QueryResponseValue.Reply,
            operation_code=0,
            authoritative_answer=False,
            truncation=False,
            recursion_desired=False,
            recursion_available=False,
            reserved=0,
            response_code=0,
            question_count=len(request.questions),
            answer_count=1,
            authority_record_count=0,
            additional_record_count=0,
        ),
        questions=request.questions,
        answers=[
            DNSAnswer(
                name="codecrafters.io",
                record_class=DNSRecordClass.IN,
                record_type=DNSRecordType.A,
                time_to_live=60,
                data=IPAddress(8,8,8,8)
            )
        ]
    )
