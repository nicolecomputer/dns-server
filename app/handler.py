from app.protocol.dns_message import DNSMessage
from app.protocol.dns_header import DNSHeader, QueryResponseValue

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
            question_count=1,
            answer_count=0,
            authority_record_count=0,
            additional_record_count=0,
        ),
        questions=request.questions,
    )
