from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()

for s in [
    b"Curve",
    b"curve",
    b"Samples",
    b"Animation",
    b"Effect"
]:
    print()
    print("====", s, "====")

    pos = 0
    total = 0

    while True:
        p = data.find(s,pos)

        if p == -1:
            break

        print(hex(p))

        print(
            data[p-64:p+128]
            .hex()
        )

        pos = p+1
        total += 1

    print("Total :", total)