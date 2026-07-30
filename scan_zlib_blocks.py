from pathlib import Path
import zlib

data = Path(
    "samples/Tendre feu v4_juillet_corrompu.c2p"
).read_bytes()

for size in [
    100000,
    200000,
    500000,
    1000000,
    2000000,
    3613445
]:

    d = zlib.decompressobj()

    try:
        out = d.decompress(
            data[62:62+size]
        )

        print(
            "Taille entrée:",
            size,
            "=> sortie:",
            len(out),
            "EOF:",
            d.eof,
            "unused:",
            len(d.unused_data)
        )

    except Exception as e:
        print(
            "Erreur taille",
            size,
            e
        )