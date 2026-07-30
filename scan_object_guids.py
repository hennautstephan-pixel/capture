from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()

objects = {
    "OBJ1":0x2d8a,
    "OBJ2":0x314e
}


def guid_scan(pos):

    start = pos-300
    end = pos+500

    print("\nZONE",hex(start),hex(end))

    for i in range(start,end):

        b=data[i:i+16]

        # UUID non nul
        if b.count(0)==0:

            print(
                hex(i),
                b.hex(" ")
            )


for name,pos in objects.items():

    print("\n======",name,"======")
    guid_scan(pos)