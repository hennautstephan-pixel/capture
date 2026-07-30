from pathlib import Path
import struct


data = Path("capture_block_full.bin").read_bytes()


objects = {
    "Ape Labs Neon Tube":0x793,
    "Plancher":0x7d6,
    "Nanlux":0x80f,
    "Plancher SKP":0x846,
    "Piano":0x883,
    "Mandarine":0x8b9,
    "Ampoule":0x8f3,
    "Pendrillons":0x92b,
    "Trussxxx":0x9e1,
    "Table":0xa17,
    "Perche":0xa4d,
    "PC face":0xab8
}


print("========== CATALOG ANALYSE ==========")


for name,offset in objects.items():

    print()
    print("----------------")
    print(name)
    print("offset",hex(offset))

    block=data[offset:offset+256]

    floats=[]

    for i in range(0,len(block)-4,4):

        v=struct.unpack(
            "<f",
            block[i:i+4]
        )[0]

        if abs(v)<1000 and v==v:
            floats.append(round(v,4))


    print(
        "floats trouvés :",
        floats[:20]
    )

    print(
        "taille bloc analysé :",
        len(block)
    )