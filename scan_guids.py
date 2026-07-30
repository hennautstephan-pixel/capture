from pathlib import Path
import uuid


data = Path(
    "capture_block_full.bin"
).read_bytes()


found=[]


for i in range(len(data)-16):

    chunk=data[i:i+16]

    try:
        u=uuid.UUID(bytes=chunk)

        # filtre GUID plausibles
        if str(u) != "00000000-0000-0000-0000-000000000000":
            found.append(
                (i,str(u))
            )

    except:
        pass


print("GUID trouvés :",len(found))


for x in found[:100]:
    print(x)