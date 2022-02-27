
def simple_message_to_str(sm) -> str:
    return "| " + str(sm.opcode) + " | " + sm.payload + " | " + str(sm.crc32) + " |"
