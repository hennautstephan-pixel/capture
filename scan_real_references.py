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


print("========== REAL REFERENCES ==========")


for name,off in objects.items():

    print()
    print("----------------")
    print(name)


    block=data[off:off+256]


    found=[]


    for i in range(0,len(block)-4,4):

        value=struct.unpack(
            "<I",
            block[i:i+4]
        )[0]


        if 0x1000 < value < len(data)-32:

            # examiner la cible

            target=data[value:value+64]


            score=0


            # présence de texte ASCII
            for c in target:
                if 32 <= c <= 126:
                    score+=1


            if score > 5:

                found.append(
                    (off+i,value,score)
                )


    for a,b,s in found:

        print(
            hex(a),
            "=>",
            hex(b),
            "score",
            s
        )


print()
print("FIN")