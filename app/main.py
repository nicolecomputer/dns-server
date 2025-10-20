import socket

from app.dns_header import DNSHeader, QueryResponseValue
from app.dns_message import DNSMessage
from app.dns_question import DNSQuestion, DNSQuestionClass, DNSQuestionType

def main():
    print("Starting up Server!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(f"Received {buf} from {source}\n")

            message = DNSMessage(
                header=DNSHeader(
                    identifier=1234,
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
                questions=[
                    DNSQuestion(
                        name="codecrafters.io",
                        question_class=DNSQuestionClass.IN,
                        question_type=DNSQuestionType.A,
                    )
                ],
            )


            print(message)
            udp_socket.sendto(message.to_bytes(), source)
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
