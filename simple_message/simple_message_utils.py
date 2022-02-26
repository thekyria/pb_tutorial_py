
def simple_message_to_str(sm):
    return "| " + str(sm.opcode) + " | " + sm.payload + " | " + str(sm.crc32) + " |"
