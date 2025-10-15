import socket


def main():
    print("Starting up Server!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(f"Received {buf} from {source}")
            response = b"Hi\n"

            udp_socket.sendto(response, source)

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
