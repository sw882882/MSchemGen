import zlib
import io
from writeUtils import *

def compress(code, LogicLinks):
    print("PROCESSORCOMPRESS.COMPRESS CALL WITH CODE:",code)
    buf = io.BytesIO(b'');
    buf.write(b'\x01')
    newCode = bytes(code, "UTF-8")
    writeInt(buf, len(newCode))
    buf.write(newCode)

    # actives coming soon
    writeInt(buf, len(LogicLinks))
    for i in LogicLinks:
        writeUTF(buf, i.name)
        writeShort(buf, i.x)
        writeShort(buf, i.y)

    result = zlib.compress(buf.getvalue())
    buf.close()
    return result
