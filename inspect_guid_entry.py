from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()


guids = {
"Ape":
bytes.fromhex(
"71 5a 99 d3 41 3d 44 4f 84 02 26 2e 76 1d 42 2a"
),

"Nanlux":
bytes.fromhex(
"3b af b0 45 f4 70 43 6d ad 12 26 13 58 f2 a4 b6"
)
}


for name,g in guids.items():

    print("\n==========",name,"==========")

    pos=data.find(g)

    print("Position :",hex(pos))

    start=pos-128
    end=pos+256

    chunk=data[start:end]

    print(chunk.hex(" "))

    print("\nASCII:")

    print(
        ''.join(
            chr(x) if 32<=x<127 else '.'
            for x in chunk
        )
    )