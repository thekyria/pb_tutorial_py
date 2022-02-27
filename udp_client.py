#!/usr/bin/env python

import argparse
import socket
from simple_message import simple_message_pb2, simple_message_utils

DEFAULT_BUFFER_SIZE = 1024
DEFAULT_LOCAL_PORT = 20212
DEFAULT_TIMEOUT = 10.0


def read_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--local-port", type=int, default=DEFAULT_LOCAL_PORT,
                        help="Port where the UDP packet will be sent from")

    parser.add_argument("-a", "--target-ip", type=str, required=True,
                        help="Target destination IP address")
    parser.add_argument("-p", "--target-port", type=int, required=True,
                        help="Target destination port")

    parser.add_argument("-b", "--buffer-size", type=int, default=DEFAULT_BUFFER_SIZE,
                        help="Size of the internal rx/tx buffer in bytes")
    args = parser.parse_args()
    return args.local_port, args.target_ip, args.target_port, args.buffer_size


def main(_local_port: int, _target_ip: str, _target_port: int, _buffer_size: int):
    print(f"udp_client[{_buffer_size}] :{_local_port} -> {_target_ip}:{_target_port}")

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as rx_tx_socket:
        rx_tx_socket.settimeout(DEFAULT_TIMEOUT)
        rx_tx_socket.bind(('', _local_port))

        message_tx = simple_message_pb2.simple_message()
        message_tx.opcode = 11
        message_tx.payload = "this is my payload"
        message_tx.crc32 = 1234
        print(f"tx ({_target_ip}:{_target_port}): {simple_message_utils.simple_message_to_str(message_tx)}")
        rx_tx_socket.sendto(message_tx.SerializeToString(), (_target_ip, _target_port))

        try:
            message_rx, address = rx_tx_socket.recvfrom(_buffer_size)
            print(f"rx ({address[0]}:{address[1]}): {message_rx.decode()}")
        except TimeoutError:
            print(f"Timeout ({DEFAULT_TIMEOUT} s)!")


if __name__ == "__main__":
    local_port, target_ip, target_port, buffer_size = read_cmd_arguments()
    main(local_port, target_ip, target_port, buffer_size)
