from pathlib import Path
import struct


data = Path(
    "capture_block_full.bin"
).read_bytes()



def read_matrix(pos):

    return struct.unpack(
        "<16f",
        data[pos:pos+64]
    )



def valid_matrix(pos):

    if pos + 64 > len(data):
        return None


    try:
        m = read_matrix(pos)

    except:
        return None



    # dernière valeur de matrice

    if abs(m[15]-1.0) > 0.001:
        return None



    x,y,z = m[12],m[13],m[14]


    if (
        abs(x) > 500 or
        abs(y) > 500 or
        abs(z) > 500
    ):
        return None



    # éliminer matrices vides

    energy=sum(
        abs(v)
        for v in m[:12]
    )


    if energy < 0.5:
        return None



    return m



results=[]



print()
print("========== SCAN GUID +18 ==========")



# on cherche les matrices possibles
# puis on regarde 18 octets avant


for matrix_pos in range(
    0,
    len(data)-64,
    4
):


    m = valid_matrix(
        matrix_pos
    )


    if not m:
        continue



    guid_pos = matrix_pos - 18


    if guid_pos < 0:
        continue



    guid = data[
        guid_pos:
        guid_pos+16
    ]



    # éviter les suites nulles

    if guid.count(0)==16:
        continue



    print()
    print(
        "GUID offset :",
        hex(guid_pos)
    )

    print(
        guid.hex(" ")
    )

    print(
        "Matrice :",
        hex(matrix_pos)
    )

    print(
        "XYZ :",
        [
            round(m[12],3),
            round(m[13],3),
            round(m[14],3)
        ]
    )


    results.append({

        "guid_offset":hex(guid_pos),

        "guid":guid.hex(),

        "matrix_offset":hex(matrix_pos)

    })



print()
print(
"Total :",
len(results)
)