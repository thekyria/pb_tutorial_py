#!/usr/bin/env python

import socket
from simple_message import simple_message_pb2, simple_message_utils

buffer_size = 1024
source_port = 20212
target_ip = "192.168.1.60"
target_port = 20060


def main():
    print("udp_client")

    rx_tx_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    rx_tx_socket.bind(('', source_port))

    message_tx = simple_message_pb2.simple_message()
    message_tx.opcode = 11
    message_tx.payload = "this is my payload"
    message_tx.crc32 = 1234
    print(f"tx ({target_ip}:{target_port}): {simple_message_utils.simple_message_to_str(message_tx)}")
    rx_tx_socket.sendto(message_tx.SerializeToString(), (target_ip, target_port))

    message_rx, address = rx_tx_socket.recvfrom(buffer_size)
    print(f"rx ({address[0]}:{address[1]}): {message_rx.decode()}")


if __name__ == "__main__":
    main()
