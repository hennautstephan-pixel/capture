from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()

guids = [
bytes.fromhex("5f b4 0e 61 2a b7 4b 58 a0 0f c7 50 47 ec 4b ae"),
bytes.fromhex("8e d0 69 1b b3 d2 4d 0b a9 9c 57 30 3d 30 10 ab")
]

for g in guids:
    print("\nGUID",g.hex())

    pos=0
    while True:
        pos=data.find(g,pos)

        if pos==-1:
            break

        print("trouvé :",hex(pos))

        # afficher 64 octets avant/après
        print(
            data[pos-64:pos+64].hex(" ")
        )

        pos+=1