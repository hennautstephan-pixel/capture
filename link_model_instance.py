from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()


instance = bytes.fromhex(
"5f b4 0e 61 2a b7 4b 58 a0 0f c7 50 47 ec 4b ae"
)

models = {
"Nanlux": bytes.fromhex(
"f2 db fd 8a 6f 6d 4e 6c be c6 75 0a 9f 24 5b 21"
),

"Ape Labs": bytes.fromhex(
"82 1c 75 08 be 3d 44 c8 93 0e 82 fc 29 e8 6e 60"
)
}


ipos=data.find(instance)

print("Instance :",hex(ipos))


zone=data[ipos-500:ipos+500]


for name,g in models.items():

    p=zone.find(g)

    print(
        name,
        p
    )