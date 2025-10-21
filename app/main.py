import socket

from app.protocol.dns_message import DNSMessage
from app.handler import handle_dns_query, DNSRecord
from app.protocol.ip_address import IPAddress
from app.protocol.dns_record_type import DNSRecordType

def main():
    print("Starting up Server!")

    known_records: list[DNSRecord] = [
        DNSRecord(
            name="codecrafters.in",
            record_type=DNSRecordType.A,
            time_to_live=60,
            data=IPAddress(8, 8, 8, 8),
        ),
    ]

    print("Known Records", known_records)


    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)

            request = DNSMessage.from_bytes(buf)
            response = handle_dns_query(known_records=known_records, request=request)

            udp_socket.sendto(response.to_bytes(), source)
            print()

            if buf == b"exit\n":
                print("Exiting\n")
                break
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

    print("Shutting down")
    udp_socket.close()


if __name__ == "__main__":
    main()
