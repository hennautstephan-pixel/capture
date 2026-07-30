from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()

guids = {
    "Ape Labs": bytes.fromhex(
        "82 1c 75 08 be 3d 44 c8 93 0e 82 fc 29 e8 6e 60"
    ),

    "Nanlux": bytes.fromhex(
        "f2 db fd 8a 6f 6d 4e 6c be c6 75 0a 9f 24 5b 21"
    )
}


for name,g in guids.items():

    print("\n====",name,"====")

    pos=0
    count=0

    while True:
        pos=data.find(g,pos)

        if pos==-1:
            break

        print(hex(pos))
        count+=1
        pos+=1

    print("Total :",count)