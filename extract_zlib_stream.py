from pathlib import Path
import zlib


data = Path(
    "samples/Tendre feu v4_juillet_corrompu.c2p"
).read_bytes()


start = 62

d = zlib.decompressobj()

output = bytearray()


chunk_size = 4096

pos = start


while pos < len(data):

    chunk = data[pos:pos+chunk_size]

    try:
        part = d.decompress(chunk)

        output.extend(part)

    except Exception as e:
        print(
            "Arrêt à",
            pos,
            e
        )
        break


    pos += chunk_size


    if d.eof:
        print(
            "FIN zlib trouvée à",
            pos
        )
        break


print(
    "Sortie totale :",
    len(output)
)


Path(
    "capture_block_full.bin"
).write_bytes(output)