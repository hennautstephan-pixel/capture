from pathlib import Path
import struct


data = Path("capture_block_full.bin").read_bytes()


targets = [
    0x65a9c,
    0xb6b98,
]


print("========== POINTERS CURVES ==========")


for t in targets:

    print()
    print("Cible :", hex(t))

    patterns = [
        struct.pack("<I", t),
        struct.pack("<Q", t)
    ]

    for ptn in patterns:

        pos = 0

        while True:

            p = data.find(ptn,pos)

            if p == -1:
                break

            print(
                "référence trouvée :",
                hex(p),
                "->",
                data[p-32:p+32].hex()
            )

            pos = p+1