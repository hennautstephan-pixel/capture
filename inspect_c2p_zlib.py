from pathlib import Path
import zlib


data = Path("Structure(1).c2p").read_bytes()


print("Taille :", len(data))


print("========== ZLIB BLOCKS ==========")


pos = 0
count = 0


while True:

    p = data.find(b'\x78\x9c', pos)

    if p == -1:
        break

    print()
    print("Bloc zlib trouvé :", hex(p))


    try:
        dec = zlib.decompress(data[p:])

        print("Taille décompressée :", len(dec))


        out = "c2p_block_%d.bin" % count

        Path(out).write_bytes(dec)

        print("Export :", out)


        # recherche texte
        for t in [
            b'Curve',
            b'curve',
            b'Samples',
            b'Object',
            b'Mesh',
            b'Group'
        ]:
            if t in dec:
                print("Trouvé :", t)


        count += 1


    except Exception as e:
        print("Erreur :", e)


    pos = p+2


print()
print("Blocs :", count)