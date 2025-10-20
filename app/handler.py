from app.protocol.dns_message import DNSMessage

DNSRequest = DNSMessage
DNSResponse = DNSMessage

def handle_dns_query(request: DNSRequest) -> DNSResponse:
    return request
