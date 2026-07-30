from pathlib import Path
import struct
import json


# =====================================================
# Chargement du fichier extrait Capture
# =====================================================

data = Path("capture_block_full.bin").read_bytes()



# =====================================================
# GUID instances validés
# =====================================================

objects = {

    "Ape Labs Neon Tube":
        "5fb40e612ab74b58a00fc75047ec4bae",

    "Nanlux":
        "8ed0691bb3d24d0ba99c57303d3010ab",

}



# =====================================================
# Lecture matrice 4x4 float32
# =====================================================

def read_matrix(pos):

    return struct.unpack(
        "<16f",
        data[pos:pos+64]
    )



# =====================================================
# Extraction matrice
#
# Structure Capture confirmée :
#
# GUID (16 octets)
# +18 octets
# = matrice 4x4
#
# =====================================================

def find_matrix(guid_pos):

    matrix_pos = guid_pos + 18


    if matrix_pos + 64 > len(data):

        return None, None


    try:

        m = read_matrix(
            matrix_pos
        )

    except:

        return None, None



    # validation matrice Capture

    if abs(m[15] - 1.0) > 0.001:

        return None, None



    return matrix_pos, m



# =====================================================
# Extraction scène
# =====================================================

scene = []


print()
print("========== EXTRACTION COMPLETE ==========")



for name, guid_hex in objects.items():


    print()
    print("-----------------------------")
    print(name)


    guid = bytes.fromhex(
        guid_hex
    )


    guid_pos = data.find(
        guid
    )


    if guid_pos == -1:

        print(
            "GUID non trouvé"
        )

        continue



    print(
        "GUID offset :",
        hex(guid_pos)
    )



    matrix_pos, matrix = find_matrix(
        guid_pos
    )



    if matrix is None:

        print(
            "Matrice non trouvée"
        )

        continue



    position = [

        round(matrix[12],4),
        round(matrix[13],4),
        round(matrix[14],4)

    ]



    rotation = [

        round(v,4)
        for v in matrix[:12]

    ]



    print(
        "Matrice offset :",
        hex(matrix_pos)
    )


    print(
        "Position :",
        position
    )


    print(
        "Rotation :",
        rotation
    )



    scene.append({

        "name": name,

        "guid_instance": guid_hex,

        "guid_offset": hex(guid_pos),

        "matrix_offset": hex(matrix_pos),

        "position": position,

        "rotation": rotation

    })



# =====================================================
# Export JSON
# =====================================================

with open(
    "capture_scene.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        scene,
        f,
        indent=4,
        ensure_ascii=False
    )



print()
print("==============================")
print(
    "Export terminé : capture_scene.json"
)
print(
    "Objets extraits :",
    len(scene)
)
print("==============================")