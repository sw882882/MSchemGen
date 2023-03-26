import io
import json
import zlib
from writeUtils import writeByte, writeShort, writeUTF, writeInt
from writeUtils import readByte, readInt, readShort, readUTF
import LogicLink
import processorCompress
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a Mindustry schematic from JSON to msch format."
    )
    parser.add_argument(
        "-i", "--input_file", metavar="input_file", type=str, help="the input JSON file"
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="output",
        type=str,
        default="a.msch",
        help="the output file (default: a.msch)",
    )
    parser.add_argument(
        "-mtj",
        "--msch_to_json",
        action="store_true",
        dest="msch_to_json",
        help="msch to json",
    )
    parser.add_argument(
        "-jtm",
        "--json_to_msch",
        action="store_true",
        dest="json_to_msch",
        help="json to msch",
    )
    return parser.parse_args()


def json_to_msch(input_file, output_file):
    # get data
    with open(input_file, "r") as f:
        data = json.load(f)

    outS = io.BytesIO(b"")

    writeShort(outS, data["width"])  # width
    writeShort(outS, data["height"])  # height

    tags = {
        "name": data["name"],
        "description": data["description"],
        "labels": json.dumps(data["tags"]),  # returns list of tags
    }

    writeByte(outS, len(tags))  # tags size
    for i in tags:
        writeUTF(outS, i)
        writeUTF(outS, tags[i])

    # blocks
    blocks = []
    for i in data["blocks"]:
        if i["type"] not in blocks:
            blocks.append(i["type"])
    print(len(blocks))
    print(blocks)
    writeByte(outS, len(blocks))
    for i in blocks:
        writeUTF(outS, i)

    # schematic tiles
    writeInt(outS, len(data["blocks"]))
    for i in data["blocks"]:
        writeByte(outS, blocks.index(i["type"]))
        writeInt(outS, i["x"] << 16 | i["y"])
        if i["type"] in ["micro-processor", "logic-processor", "hyper-processor"]:
            # set up links
            links = []
            for j in i["config"]["links"]:
                links += [LogicLink.LogicLink(j["x"], j["y"], j["name"], True)]
            if i["config"]["code"].startswith("code:"):
                with open(i["config"]["code"][5:], "r") as f:
                    code = f.read()
            else:
                code = i["config"]["code"]
            writeByte(outS, 14)
            more_data = processorCompress.compress(code, links)
            writeInt(outS, len(more_data))
            outS.write(more_data)
        # TODO fix this
        # elif i["type"] in [
        #    "bridge-conveyor",
        #    "phase-conveyor",
        #    "mass-driver",
        #    "large-payload-mass-driver",
        #    "payload-mass-driver",
        #    "bridge-conduit",
        #    "phase-conduit",
        # ]:
        # blocks that link two things (basically bridges)
        # setup links, should only have one link

        else:
            writeByte(outS, 3)
            writeInt(outS, 0)

        writeByte(outS, i["rotation"])

    # finishing
    data = b"msch\x01" + zlib.compress(outS.getvalue())
    with open(output_file, "wb") as f:
        f.write(data)
    outS.close()


def msch_to_json(input_file, output_file):
    # get msch file
    with open(input_file, "rb") as f:
        data = f.read()
    data = io.BytesIO(zlib.decompress(data[len("msch\x01") :]))

    width = readShort(data)
    height = readShort(data)

    length_of_tag = readByte(data)

    readUTF(data)
    name = readUTF(data)
    readUTF(data)
    description = readUTF(data)
    readUTF(data)
    labels = readUTF(data)

    no_of_type_of_blocks = readByte(data)

    block_types = []
    for i in range(no_of_type_of_blocks):
        block_types.append(readUTF(data))

    no_of_blocks = readInt(data)

    blocks = []
    for i in range(no_of_blocks):
        block = block_types[readByte(data)]
        val = readInt(data)
        x = val >> 16
        y = val & 0xFFFF
        # TODO if has config something something then do this if else do the config
        readByte(data)
        readInt(data)
        rotation = readByte(data)

        blocks.append(
            {"type": block, "x": x, "y": y, "rotation": rotation, "config": 0}  # TODO
        )

    json_data = {
        "name": name,
        "description": description,
        "tags": json.loads(labels),
        "width": width,
        "height": height,
        "blocks": blocks,
    }

    print(json.dumps(json_data, sort_keys=False, indent=4))


def main():
    args = parse_args()
    if args.json_to_msch:
        json_to_msch(args.input_file, args.output)
    elif args.msch_to_json:
        msch_to_json(args.input_file, args.output)


if __name__ == "__main__":
    main()
