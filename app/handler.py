from app.protocol.dns_message import DNSMessage
from app.protocol.dns_header import (
    DNSHeader,
    QueryResponseValue,
    QueryOpcode,
    ResponseOpcode,
)
from app.protocol.dns_answer import DNSAnswer
from app.protocol.dns_question import DNSQuestion
from app.records import DNSRecord, find_records


DNSRequest = DNSMessage
DNSResponse = DNSMessage


def answer_dns_question(
    known_records: list[DNSRecord], question: DNSQuestion
) -> list[DNSAnswer]:
    records = find_records(
        known_records, name=question.name, record_type=question.record_type
    )

    return [record.to_dns_answer() for record in records]


def is_authoritative(
    known_records: list[DNSRecord], questions: list[DNSQuestion]
) -> bool:
    for question in questions:
        records = find_records(known_records, name=question.name)
        if len(records) == 0:
            return False

    return True


def not_implemented_response_from(request: DNSRequest) -> DNSResponse:
    return DNSResponse(
        header=DNSHeader(
            identifier=request.header.identifier,
            query_response_indicator=QueryResponseValue.Reply,
            operation_code=request.header.operation_code,
            authoritative_answer=False,
            truncation=False,
            recursion_desired=request.header.recursion_desired,
            recursion_available=False,
            reserved=0,
            response_code=ResponseOpcode.NotImplemented,
            question_count=len(request.questions),
            answer_count=0,
            authority_record_count=0,
            additional_record_count=0,
        ),
        questions=request.questions,
        answers=[],
    )


def refused_response_from(request: DNSRequest) -> DNSResponse:
    return DNSResponse(
        header=DNSHeader(
            identifier=request.header.identifier,
            query_response_indicator=QueryResponseValue.Reply,
            operation_code=request.header.operation_code,
            authoritative_answer=False,
            truncation=False,
            recursion_desired=request.header.recursion_desired,
            recursion_available=False,
            reserved=0,
            response_code=ResponseOpcode.Refused,
            question_count=len(request.questions),
            answer_count=0,
            authority_record_count=0,
            additional_record_count=0,
        ),
        questions=request.questions,
        answers=[],
    )


def handle_dns_query(
    known_records: list[DNSRecord], request: DNSRequest
) -> DNSResponse:
    if request.header.operation_code != QueryOpcode.Query:
        return not_implemented_response_from(request=request)

    questions = request.questions
    is_authoritative_for_records = is_authoritative(
        known_records=known_records, questions=questions
    )

    if not is_authoritative_for_records:
        return refused_response_from(request=request)

    answers = []
    for question in questions:
        answers += answer_dns_question(known_records=known_records, question=question)

    return DNSResponse(
        header=DNSHeader(
            identifier=request.header.identifier,
            query_response_indicator=QueryResponseValue.Reply,
            operation_code=request.header.operation_code,
            authoritative_answer=is_authoritative_for_records,
            truncation=False,
            recursion_desired=request.header.recursion_desired,
            recursion_available=False,
            reserved=0,
            response_code=ResponseOpcode.NoError,
            question_count=len(request.questions),
            answer_count=len(answers),
            authority_record_count=0,
            additional_record_count=0,
        ),
        questions=questions,
        answers=answers,
    )
