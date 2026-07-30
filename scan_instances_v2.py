from pathlib import Path
import struct
import json
import re


data = Path(
    "capture_block_full.bin"
).read_bytes()



def read_matrix(pos):

    return struct.unpack(
        "<16f",
        data[pos:pos+64]
    )



def test_matrix(pos):

    if pos+64 > len(data):
        return None


    try:
        m = read_matrix(pos)

    except:
        return None


    # Capture utilise une matrice avec dernier float = 1

    if abs(m[15]-1.0) > 0.001:
        return None


    x,y,z = m[12],m[13],m[14]


    if (
        abs(x)>500 or
        abs(y)>500 or
        abs(z)>500
    ):
        return None


    return {
        "offset":hex(pos),
        "position":[
            round(x,4),
            round(y,4),
            round(z,4)
        ]
    }



results=[]


print()
print("========== SCAN GUID INSTANCES ==========")



# recherche des blocs 01 01 01 + GUID

for m in re.finditer(
    rb'\x01\x01\x01(.{16})',
    data
):

    guid_pos = m.start()+3

    matrix_pos = guid_pos + 18


    mat=test_matrix(
        matrix_pos
    )


    if mat:


        print()
        print(
            "GUID :",
            hex(guid_pos)
        )

        print(
            "Matrice :",
            mat["offset"]
        )

        print(
            "Position :",
            mat["position"]
        )


        results.append({

            "guid_offset":hex(guid_pos),

            "matrix":mat

        })



print()
print(
"Instances trouvées :",
len(results)
)



with open(
    "instances_scan.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )