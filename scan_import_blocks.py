from pathlib import Path
import struct


data = Path("capture_block_full.bin").read_bytes()


objects = {
    "Plancher SKP":0x846,
    "Trussxxx":0x9e1,
    "Table":0xa17,
    "Perche":0xa4d,
    "PC face":0xab8
}


print("========== IMPORT BLOCKS ==========")


for name,off in objects.items():

    print()
    print("----------------")
    print(name)

    block=data[off:off+512]

    # chercher des valeurs ressemblant à une taille
    sizes=[]

    for i in range(0,len(block)-4,4):

        v=struct.unpack(
            "<I",
            block[i:i+4]
        )[0]

        if 1000 < v < 2000000:
            sizes.append(
                (hex(off+i),v)
            )

    for x in sizes[:10]:
        print(x)
