from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()

for t in [
    b"structure",
    b"Structure",
    b".c2p",
    b"SketchUp",
    b"SKP",
    b"Plancher",
    b"Table"
]:
    print()
    print("====", t, "====")

    pos=0
    total=0

    while True:
        p=data.find(t,pos)

        if p==-1:
            break

        print(hex(p))
        pos=p+1
        total+=1

    print("Total :",total)