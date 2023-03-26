def writeByte(out, val):
    out.write(bytes([val & 255]))
    # print("Written byte", hex(val & 0xFF))
    print(out.getvalue())


def writeShort(out, val):
    # print("WRITESHORT CALL")
    writeByte(out, val >> 8)
    writeByte(out, val & 0xFF)


def writeInt(out, val):
    # print("WRITEINT CALL")
    writeByte(out, val >> 24)
    writeByte(out, val >> 16 & 0xFF)
    writeByte(out, val >> 8 & 0xFF)
    writeByte(out, val & 0xFF)


def writeUTF(out, val):
    # print("WRITEUTF CALL")
    if isinstance(val, bytes):
        val2 = val
    else:
        val2 = bytes(val, "UTF-8")
    writeShort(out, len(val2))
    out.write(val2)
    # print("Written", val2)
    print(out.getvalue())


def readByte(stream):
    byte = stream.read(1)
    if not byte:
        return None
    return byte[0]


def readShort(stream):
    high_byte = readByte(stream)
    low_byte = readByte(stream)
    if high_byte is None or low_byte is None:
        return None
    val = (high_byte << 8) | low_byte
    return val


def readInt(stream):
    b1 = readByte(stream)
    b2 = readByte(stream)
    b3 = readByte(stream)
    b4 = readByte(stream)
    if b1 is None or b2 is None or b3 is None or b4 is None:
        return None
    val = (b1 << 24) | (b2 << 16) | (b3 << 8) | b4
    return val


def readUTF(stream):
    length = readShort(stream)
    if length is None:
        return None
    bytes_seq = stream.read(length)
    if len(bytes_seq) != length:
        return None
    val = bytes_seq.decode("UTF-8")
    return val
