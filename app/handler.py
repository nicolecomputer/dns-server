from app.protocol.dns_message import DNSMessage
from app.protocol.dns_header import DNSHeader, QueryResponseValue, QueryOpcode, ResponseOpcode
from app.protocol.dns_answer import DNSAnswer
from app.protocol.ip_address import IPAddress
from app.protocol.dns_question import DNSQuestion
from app.protocol.dns_answer import DNSAnswer

DNSRequest = DNSMessage
DNSResponse = DNSMessage

def answer_dns_question(question: DNSQuestion) -> DNSAnswer:
    match (question.name, question.record_class, question.record_type):
        case ("codecrafters.io", "IN", "A"):
            return DNSAnswer(
                name=question.name,
                record_class=question.record_class,
                record_type=question.record_type,
                time_to_live=60,
                data=IPAddress(8,8,8,8)
            )

    return DNSAnswer(
            name=question.name,
            record_class=question.record_class,
            record_type=question.record_type,
            time_to_live=60,
            data=IPAddress(8,8,8,8)
        )

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
        answers=[]
    )


def handle_dns_query(request: DNSRequest) -> DNSResponse:
    if request.header.operation_code != QueryOpcode.Query:
        return not_implemented_response_from(request=request)

    questions = request.questions
    answers = [answer_dns_question(question) for question in questions]

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
            response_code=ResponseOpcode.NoError,
            question_count=len(request.questions),
            answer_count=len(answers),
            authority_record_count=0,
            additional_record_count=0,
        ),
        questions=questions,
        answers=answers
    )
