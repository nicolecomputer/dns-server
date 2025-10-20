import pprint
import socket

from app.protocol.dns_message import DNSMessage

from app.handler import handle_dns_query

def main():
    print("Starting up Server!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)

            request = DNSMessage.from_bytes(buf)
            response = handle_dns_query(request)
            print("REQUEST: ")
            pprint.pp(request.__dict__, width=100, indent=1)
            print("RESPONSE: ")
            pprint.pp(response.__dict__, width=100, indent=1)
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
