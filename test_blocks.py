import zlib

data = open(
    r"samples\Tendre feu v4_juillet_corrompu.c2p",
    "rb"
).read()


for start in [62, 64, 68]:

    print("\nOFFSET", start)

    for size in [
        0x1000,
        0x2000,
        0x4000,
        0x8000,
        0x10000
    ]:
        block = data[start:start+size]

        try:
            out = zlib.decompress(block)

            print(
                "DECOMP OK",
                hex(size),
                "=>",
                len(out)
            )

        except Exception as e:
            pass