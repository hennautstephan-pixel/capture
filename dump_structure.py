from pathlib import Path

data = Path("capture_block_full.bin").read_bytes()


def dump(start,end):
    for i in range(start,end,16):
        print(
            f"{i:08X}",
            data[i:i+16].hex(" ")
        )


dump(11300,11780)