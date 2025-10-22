import socket

from app.client.dns_client import DNSServer
from app.handler import handle_dns_query
from app.protocol.dns_message import DNSMessage
from app.protocol.dns_record_type import DNSRecordType
from app.protocol.ip_address import IPAddress
from app.records import DNSRecord


def main() -> None:
    print("Starting up Server!")

    known_records: list[DNSRecord] = [
        DNSRecord(
            name="codecrafters.io",
            record_type=DNSRecordType.A,
            time_to_live=60,
            data=IPAddress(8, 8, 8, 8),
        ),
        DNSRecord(
            name="abc.codecrafters.io",
            record_type=DNSRecordType.A,
            time_to_live=60,
            data=IPAddress(8, 8, 8, 8),
        ),
        DNSRecord(
            name="abc.longassdomainname.com",
            record_type=DNSRecordType.A,
            time_to_live=60,
            data=IPAddress(9, 9, 9, 9),
        ),
        DNSRecord(
            name="def.longassdomainname.com",
            record_type=DNSRecordType.A,
            time_to_live=60,
            data=IPAddress(12, 12, 12, 12),
        ),
        DNSRecord(
            name="reddit.com",
            record_type=DNSRecordType.A,
            time_to_live=61,
            data=IPAddress(151, 101, 129, 140),
        ),
        DNSRecord(
            name="mail.example.com",
            record_type=DNSRecordType.A,
            time_to_live=61,
            data=IPAddress(8, 8, 8, 8),
        ),
        DNSRecord(
            name="example.com",
            record_type=DNSRecordType.A,
            time_to_live=61,
            data=IPAddress(8, 8, 8, 8),
        ),
        DNSRecord(
            name="alt1.aspmx.l.google.com",
            record_type=DNSRecordType.A,
            time_to_live=61,
            data=IPAddress(8, 8, 8, 8),
        ),
        DNSRecord(
            name="google.com",
            record_type=DNSRecordType.A,
            time_to_live=61,
            data=IPAddress(8, 8, 8, 8),
        ),
    ]

    backup_server = DNSServer(address=IPAddress(8, 8, 8, 8), port=53)

    print("Known Records", known_records)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 2053))

    while True:
        buf, source = udp_socket.recvfrom(512)

        request = DNSMessage.from_bytes(buf)
        response = handle_dns_query(
            known_records=known_records, server=backup_server, request=request
        )

        udp_socket.sendto(response.to_bytes(), source)
        print()

        if buf == b"exit\n":
            print("Exiting\n")
            break

    print("Shutting down")
    udp_socket.close()


if __name__ == "__main__":
    main()
