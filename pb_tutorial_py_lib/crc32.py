
import zlib


def calculate_crc(message: str) -> int:
    return int(hex(zlib.crc32(message.encode()) & 0xffffffff), 0)
