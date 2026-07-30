from pathlib import Path
import struct


data = Path(
    "capture_block_full.bin"
).read_bytes()


results=[]


for i in range(0,len(data)-64,4):

    vals = struct.unpack(
        "<16f",
        data[i:i+64]
    )


    # vraie matrice homogène
    if abs(vals[15]-1.0)<0.001:

        x,y,z = vals[12],vals[13],vals[14]


        if (
            abs(x)<100
            and abs(y)<100
            and abs(z)<100
        ):

            results.append(
                (
                    i,
                    round(x,3),
                    round(y,3),
                    round(z,3)
                )
            )


print(
    "Transformations trouvées :",
    len(results)
)


for r in results[:100]:
    print(r)