from pathlib import Path


data = Path("capture_block_full.bin").read_bytes()


targets = {
    "Trussxxx":0x6a221,
    "Table":0x71c7c
}


for name, offset in targets.items():

    print()
    print("====================")
    print(name)
    print("OFFSET :", hex(offset))
    print("====================")

    block = data[offset:offset+512]

    print(block.hex())

    print()
    print("ASCII:")

    txt=""

    for b in block:
        if 32 <= b <= 126:
            txt += chr(b)
        else:
            txt += "."

    print(txt)