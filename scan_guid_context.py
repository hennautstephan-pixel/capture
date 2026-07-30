from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()


guids = {
"INSTANCE_NANLUX?": bytes.fromhex(
"5f b4 0e 61 2a b7 4b 58 a0 0f c7 50 47 ec 4b ae"
),

"MODEL_NANLUX": bytes.fromhex(
"f2 db fd 8a 6f 6d 4e 6c be c6 75 0a 9f 24 5b 21"
),

"MODEL_APE": bytes.fromhex(
"82 1c 75 08 be 3d 44 c8 93 0e 82 fc 29 e8 6e 60"
)
}


for name,g in guids.items():

    print("\n======",name,"======")

    pos=0

    while True:

        pos=data.find(g,pos)

        if pos==-1:
            break

        print("Offset :",hex(pos))

        start=max(0,pos-200)
        end=min(len(data),pos+200)

        print(
            data[start:end].hex(" ")
        )

        pos+=16