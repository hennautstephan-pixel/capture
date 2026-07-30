from pathlib import Path
import struct


base = Path("samples/1 projecteur.bin").read_bytes()
move = Path("samples/1 projecteur_deplacement.bin").read_bytes()


offsets = [
    0x2bf8,
    0x2cfc,
    0x2d51,
    0x2d61,
    0x2d71
]


for off in offsets:

    print()
    print("================")
    print(hex(off))
    print("================")

    print("BASE")

    for i in range(0,16,4):
        print(
            struct.unpack(
                "<f",
                base[off+i:off+i+4]
            )[0]
        )


    print("DEPLACEMENT")

    for i in range(0,16,4):
        print(
            struct.unpack(
                "<f",
                move[off+i:off+i+4]
            )[0]
        )