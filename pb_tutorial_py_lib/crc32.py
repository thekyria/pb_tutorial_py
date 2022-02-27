
import zlib


def calculate_crc(message: str) -> int:
    return zlib.crc32(message.encode())
