from pathlib import Path
import struct


data = Path(
    "capture_block_full.bin"
).read_bytes()


print("Taille :", len(data))


print()
print("========== POSSIBLE CURVES ==========")


found = 0


for offset in range(0, len(data)-40, 4):

    count = struct.unpack_from(
        "<I",
        data,
        offset
    )[0]


    # tailles plausibles de courbes
    if count < 2 or count > 64:
        continue


    values = []

    valid = True


    for i in range(count * 2):

        p = offset + 4 + i*4

        if p+4 > len(data):
            valid=False
            break

        v = struct.unpack_from(
            "<f",
            data,
            p
        )[0]


        if abs(v) > 100000:
            valid=False
            break

        values.append(v)


    if valid and len(values) >= 4:

        print()
        print(
            "Offset",
            hex(offset),
            "Samples",
            count
        )

        print(
            values[:10]
        )


        found += 1


        if found > 50:
            break


print()
print(
    "Trouvés :",
    found
)