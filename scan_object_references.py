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


print("========== REFERENCES OBJETS ==========")


for name, off in objects.items():

    print()
    print("----------------")
    print(name)
    print("Catalogue :",hex(off))


    block=data[off:off+128]


    for i in range(0,len(block)-4,4):

        val=struct.unpack(
            "<I",
            block[i:i+4]
        )[0]


        # offsets plausibles dans le fichier
        if 0x1000 < val < len(data):

            print(
                "possible offset",
                hex(off+i),
                "=>",
                hex(val)
            )