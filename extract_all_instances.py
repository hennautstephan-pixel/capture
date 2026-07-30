from pathlib import Path
import struct
import json
import re


data = Path(
    "capture_block_full.bin"
).read_bytes()



# =====================================================
# Objets catalogue connus
# =====================================================

objects = [

    "Ape Labs Neon Tube",
    "Plancher",
    "Nanlux",
    "Plancher SKP",
    "Piano",
    "Mandarine",
    "Ampoule",
    "Pendrillons",
    "Trussxxx",
    "Table",
    "Perche",
    "PC face"

]



# =====================================================
# Lecture matrice
# =====================================================

def read_matrix(pos):

    return struct.unpack(
        "<16f",
        data[pos:pos+64]
    )



# =====================================================
# Recherche matrice après GUID
# règle validée :
# GUID +18
# =====================================================

def get_matrix(guid_pos):

    pos = guid_pos + 18


    if pos+64 > len(data):
        return None


    try:

        m = read_matrix(pos)

    except:

        return None



    if abs(m[15]-1.0)>0.001:

        return None


    return {

        "offset":hex(pos),

        "position":[
            round(m[12],4),
            round(m[13],4),
            round(m[14],4)
        ],

        "rotation":[
            round(x,4)
            for x in m[:12]
        ]

    }



# =====================================================
# Recherche GUID modèle proche du nom
# =====================================================

def find_object(name):


    name_bytes = name.encode(
        "utf-8"
    )


    pos = data.find(
        name_bytes
    )


    if pos == -1:

        return None



    # Cherche le GUID instance
    # situé après le nom


    block = data[pos:pos+150]


    # GUID 16 octets
    # précédé de 01 01 01


    for m in re.finditer(
        rb'\x01\x01\x01(.{16})',
        block
    ):


        guid_pos = pos + m.start()+3


        matrix = get_matrix(
            guid_pos
        )


        if matrix:


            return {

                "name":name,

                "name_offset":hex(pos),

                "guid_offset":hex(guid_pos),

                "guid":
                    block[m.start()+3:m.start()+19].hex(),

                "matrix":matrix

            }


    return None



# =====================================================
# Extraction
# =====================================================


scene=[]


print()
print(
"========== SCENE COMPLETE =========="
)



for obj in objects:


    print()
    print("----------------")

    print(obj)


    result=find_object(
        obj
    )


    if result:


        print(
            "GUID :",
            result["guid"]
        )

        print(
            "Matrice :",
            result["matrix"]["offset"]
        )

        print(
            "Position :",
            result["matrix"]["position"]
        )


        scene.append(
            result
        )


    else:

        print(
            "Non trouvé"
        )



# =====================================================
# Export
# =====================================================


with open(
    "capture_scene_full.json",
    "w",
    encoding="utf8"
) as f:


    json.dump(
        scene,
        f,
        indent=4,
        ensure_ascii=False
    )



print()
print(
"Objets extraits :",
len(scene)
)

print(
"Fichier : capture_scene_full.json"
)