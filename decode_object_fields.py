from pathlib import Path
import struct


data = Path("samples/1 projecteur.bin").read_bytes()


offsets = [
    0x2591,
    0x2bf8,
    0x2cfc,
    0x2d51,
    0x2d61,
    0x2d71,
    0x30b2
]


for off in offsets:

    print()
    print("================")
    print(hex(off))
    print("================")

    b=data[off:off+16]

    print("HEX :", b.hex())


    if len(b)>=4:
        print(
            "float32:",
            struct.unpack("<f",b[:4])[0]
        )

        print(
            "uint32:",
            struct.unpack("<I",b[:4])[0]
        )


    if len(b)>=8:
        print(
            "double:",
            struct.unpack("<d",b[:8])[0]
        )