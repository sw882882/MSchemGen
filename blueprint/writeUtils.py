def writeByte(out, val):
    out.write(bytes([val & 255]))
    print("Written byte", hex(val & 0xFF))

def writeShort(out, val):
    print("WRITESHORT CALL")
    writeByte(out, val >> 8)
    writeByte(out, val & 0xFF)

def writeInt(out, val):
    print("WRITEINT CALL")
    writeByte(out, val >> 24)
    writeByte(out, val >> 16 & 0xFF)
    writeByte(out, val >> 8 & 0xFF)
    writeByte(out, val & 0xFF)

def writeUTF(out, val):
    print("WRITEUTF CALL")
    if isinstance(val, bytes): val2 = val
    else: val2 = bytes(val, 'UTF-8')
    writeShort(out, len(val2))
    out.write(val2)
    print("Wrriten", val2)