#!/usr/bin/env python

import socket
from simple_message import simple_message_pb2, simple_message_utils

local_ip = '0.0.0.0'
local_port = 20212
buffer_size = 1024


def main():
    print("udp_server")

    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind((local_ip, local_port))
    while True:

        message_rx_raw, address = udp_server_socket.recvfrom(buffer_size)
        message_rx = simple_message_pb2.simple_message()
        message_rx.ParseFromString(message_rx_raw)
        message_rx_str = simple_message_utils.simple_message_to_str(message_rx)
        print(f"rx ({address}): {message_rx_str} (raw: {message_rx_raw})")

        # Sending a reply to client
        message_tx = "ACK " + message_rx_str
        udp_server_socket.sendto(str.encode(message_tx), address)
        print(f"tx ({address}): {message_tx}")


if __name__ == "__main__":
    main()
