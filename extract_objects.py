from pathlib import Path
import struct
import math


# ==========================
# Chargement du bloc extrait
# ==========================

data = Path("capture_block_full.bin").read_bytes()



# ==========================
# Vérification matrice 4x4
# ==========================

def is_matrix(vals):

    # dernière valeur = 1
    if abs(vals[15] - 1.0) > 0.001:
        return False


    # éliminer matrice identité
    identity = [
        1,0,0,0,
        0,1,0,0,
        0,0,1,0,
        0,0,0,1
    ]

    if all(
        abs(vals[i]-identity[i]) < 0.001
        for i in range(16)
    ):
        return False


    # coordonnées
    x,y,z = vals[12], vals[13], vals[14]


    # limites physiques
    if abs(x)>1000 or abs(y)>1000 or abs(z)>1000:
        return False


    # vérifier axes rotation normalisés

    axes = [
        (0,1,2),
        (4,5,6),
        (8,9,10)
    ]


    for a,b,c in axes:

        length = math.sqrt(
            vals[a]**2 +
            vals[b]**2 +
            vals[c]**2
        )

        if abs(length-1)>0.05:
            return False


    return True



# ==========================
# Objets connus
#
# début GUID instance
# fin bloc objet
# ==========================

objects = [

    (
        "Ape Labs Neon Tube",
        0x2d8a,
        0x2f00
    ),

    (
        "Nanlux",
        0x314e,
        0x3300
    )

]



# ==========================
# Extraction
# ==========================


for name,guid_pos,end_pos in objects:


    print("\n================")
    print(name)
    print("================")


    start = guid_pos
    end = end_pos


    results=[]


    for pos in range(start,end):


        if pos + 64 > len(data):
            continue


        try:

            vals = struct.unpack(
                "<16f",
                data[pos:pos+64]
            )

        except:

            continue



        if is_matrix(vals):


            x,y,z = vals[12:15]


            results.append(
                (
                    pos,
                    x,
                    y,
                    z,
                    vals
                )
            )



    # suppression doublons proches

    filtered=[]


    for item in results:


        if not filtered:

            filtered.append(item)


        else:

            if abs(item[0]-filtered[-1][0]) > 16:

                filtered.append(item)



    for pos,x,y,z,mat in filtered:


        print(
            hex(pos),
            "XYZ =",
            round(x,3),
            round(y,3),
            round(z,3)
        )


        print(
            "Rotation :"
        )

        print(
            [
                round(v,4)
                for v in mat[:12]
            ]
        )