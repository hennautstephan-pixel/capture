from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()

terms = [
    b"Nanlux",
    b"Evoke",
    b"600C",
    b"Ape Labs",
    b"Neon",
    b"Fixture",
    b"Profile",
    b"Channel",
    b"Dimmer"
]


for t in terms:

    print()
    print("==========", t, "==========")

    pos = 0
    n = 0

    while True:

        p = data.find(t,pos)

        if p < 0:
            break

        print(hex(p))

        print(
            data[p-80:p+120]
            .hex()
        )

        pos=p+1
        n+=1

    print("Total :",n)