import sys
import io
import json
import base64
import zlib
from writeUtils import *
import LogicLink
import processorCompress

# get data
f = open(sys.argv[1], "r")
data = json.loads(f.read())
f.close()

outS = io.BytesIO(b'')

writeShort(outS, data["width"]) # width
writeShort(outS, data["height"]) # height

tags = {
        "name" : data["name"],
        "description" : data["description"],
        "labels" : json.dumps(data["tags"]),
}

writeByte(outS, len(tags)) # tags size
for i in tags:
    writeUTF(outS, i)
    writeUTF(outS, tags[i])

# blocks
blocks = []
for i in data["blocks"]:
    if i["type"] not in blocks:
        blocks.append(i["type"])
writeByte(outS, len(blocks))
for i in blocks: writeUTF(outS, i)

# schematic tiles
writeInt(outS, len(data["blocks"]))
for i in data["blocks"]:
    writeByte(outS, blocks.index(i["type"]))
    writeInt(outS, i["x"] << 16 | i["y"])
    if i["type"] in ["micro-processor","logic-processor","hyper-processor"]:
        # set up links
        links = []
        for j in i["links"]:
            links += [LogicLink.LogicLink(j["x"],j["y"],j["name"],True)]

        writeByte(outS, 14)
        more_data = processorCompress.compress(i["code"], links)
        writeInt(outS, len(more_data))
        outS.write(more_data)
    else:
        writeByte(outS, 3)
        writeInt(outS, 0)

    writeByte(outS, i["rotation"])

# finishing
aaaa = open("a.msch", "wb")
data = b'msch\x01'+zlib.compress(outS.getvalue())
# data = base64.b64encode(data)
aaaa.write(data)
aaaa.close()
# print(str((b'msch\x01'+zlib.compress(outS.getvalue())),"UTF-8"))
outS.close()
