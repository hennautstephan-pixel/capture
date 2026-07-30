from pathlib import Path
import zlib


BASE = Path("samples")


FILES = [
    BASE / "1 projecteur.c2p",
    BASE / "1 projecteur_rotation.c2p",
    BASE / "1 projecteur_deplacement.c2p",
    BASE / "1 projecteur_dmx.c2p",
]


def extract(path):

    print()
    print("====================")
    print(path.name)
    print("====================")

    data = path.read_bytes()

    print("Taille :", len(data))

    pos = data.find(b"\x78\x9c")

    if pos == -1:
        print("Pas de bloc zlib")
        return


    print("Zlib offset :", hex(pos))


    try:

        decoded = zlib.decompress(data[pos:])

        print(
            "Taille décompressée :",
            len(decoded)
        )


        out = path.with_suffix(".bin")

        out.write_bytes(decoded)

        print(
            "Export :",
            out
        )


    except Exception as e:

        print(
            "Erreur décompression :",
            e
        )


for f in FILES:

    if f.exists():
        extract(f)

    else:
        print()
        print("MANQUANT :", f)