from app.protocol.dns_header import DNSHeader, QueryResponseValue, QueryOpcode, ResponseOpcode
def test_building_a_header():

    header = DNSHeader(
        identifier=1234,
        query_response_indicator=QueryResponseValue.Reply,
        operation_code=QueryOpcode.Query,
        authoritative_answer=True,
        truncation=False,
        recursion_desired=False,
        recursion_available=False,
        reserved=0,
        response_code=ResponseOpcode.NoError,
        question_count=0,
        answer_count=0,
        authority_record_count=0,
        additional_record_count=0
    )
    data = header.to_bytes()

    assert data.hex() == '04d284000000000000000000'
