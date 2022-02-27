#!/usr/bin/env python

import argparse
import socket
from simple_message import simple_message_pb2, simple_message_utils

DEFAULT_LOCAL_IP = '0.0.0.0'
DEFAULT_LOCAL_PORT = 20212
DEFAULT_BUFFER_SIZE = 1024


def read_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--local-ip", type=str, default=DEFAULT_LOCAL_IP,
                        help="IP where the local server is going to listen to")
    parser.add_argument("-p", "--local-port", type=int, default=DEFAULT_LOCAL_PORT,
                        help="Port where the local server is going to listen to")
    parser.add_argument("-b", "--buffer-size", type=int, default=DEFAULT_BUFFER_SIZE,
                        help="Size of the internal rx/tx buffer in bytes")
    args = parser.parse_args()
    return args.local_ip, args.local_port, args.buffer_size


def main(_local_ip: str, _local_port: int, _buffer_size: int) -> None:
    print(f"udp_server[{_buffer_size}] {_local_ip}:{_local_port}")

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as udp_server_socket:
        udp_server_socket.bind((_local_ip, _local_port))

        # try:
        while True:
            message_rx_raw, address = udp_server_socket.recvfrom(_buffer_size)
            message_rx = simple_message_pb2.simple_message()
            message_rx.ParseFromString(message_rx_raw)
            message_rx_str = simple_message_utils.simple_message_to_str(message_rx)
            print(f"rx ({address}): {message_rx_str} (raw: {message_rx_raw})")

            # Sending a reply to client
            message_tx = "ACK " + message_rx_str
            udp_server_socket.sendto(str.encode(message_tx), address)
            print(f"tx ({address}): {message_tx}")
        # except KeyboardInterrupt:
        #     print("shutting server")


if __name__ == "__main__":
    local_ip, local_port, buffer_size = read_cmd_arguments()
    main(local_ip, local_port, buffer_size)
