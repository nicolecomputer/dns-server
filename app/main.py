import socket

from app.dns_header import DNSHeader, QueryResponseValue


def main():
    print("Starting up Server!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(f"Received {buf} from {source}\n")

            header = DNSHeader(
                identifier=1234,
                query_response_indicator=QueryResponseValue.Reply,
                operation_code=0,
                authoritative_answer=False,
                truncation=False,
                recursion_desired=False,
                recursion_available=False,
                reserved=0,
                response_code=0,
                question_count=0,
                answer_count=0,
                authority_record_count=0,
                additional_record_count=0
            )

            udp_socket.sendto(header.to_bytes(), source)

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
