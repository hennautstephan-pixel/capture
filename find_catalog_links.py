from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()


guids = {
    "OBJ1 second GUID":
    bytes.fromhex(
        "71 5a 99 d3 41 3d 44 4f 84 02 26 2e 76 1d 42 2a"
    ),

    "OBJ2 catalog GUID":
    bytes.fromhex(
        "3b af b0 45 f4 70 43 6d ad 12 26 13 58 f2 a4 b6"
    )
}


for name,g in guids.items():

    print("\n",name)

    pos=0

    while True:
        pos=data.find(g,pos)

        if pos==-1:
            break

        print("trouvé :",hex(pos))
        pos+=1