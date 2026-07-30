import zlib

data = open(
    r"samples\Tendre feu v4_juillet_corrompu.c2p",
    "rb"
).read()

# recherche des signatures zlib
positions = []

for i in range(len(data)-2):
    if data[i] == 0x78 and data[i+1] in (0x01,0x5e,0x9c,0xda):
        positions.append(i)

print("Signatures trouvées :", len(positions))
print(positions[:20])


for start in positions[:20]:

    print("\nTest offset :", start)

    for size in [256,512,1024,2048,4096,8192,16384,32768,65536,131072]:

        try:
            d = zlib.decompressobj()
            out = d.decompress(data[start:start+size])

            if d.eof:
                print(
                    "OK",
                    "taille compressée",
                    size,
                    "taille sortie",
                    len(out)
                )
                break

        except:
            pass