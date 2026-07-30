from pathlib import Path
import struct
import re


# ==================================================
# Chargement fichier
# ==================================================

data = Path("capture_block_full.bin").read_bytes()


# ==================================================
# Objets connus du catalogue Capture
# ==================================================

object_names = [
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
    "PC face",
]


catalog = {}



# ==================================================
# Extraction catalogue
# ==================================================

print("========== CATALOGUE ==========")


for name in object_names:

    pos = data.find(
        name.encode("utf-8")
    )

    if pos == -1:
        continue


    zone = data[pos:pos+250]


    guid = None


    # Recherche GUID réel
    for i in range(len(zone)-16):

        candidate = zone[i:i+16]


        ascii_count = sum(
            32 <= b <= 126
            for b in candidate
        )


        # GUID Capture :
        # peu de caractères ASCII
        # peu de zéros
        if (
            ascii_count < 8
            and candidate.count(b"\x00") < 5
        ):

            guid = candidate
            break



    if guid:

        catalog[guid] = name

        print(
            name,
            guid.hex()
        )


print()
print("Objets catalogue :",len(catalog))



# ==================================================
# Recherche instances
# ==================================================

print()
print("========== INSTANCES ==========")



def read_matrix(offset):

    try:

        values = struct.unpack(
            "<16f",
            data[offset:offset+64]
        )

        return values

    except:

        return None




for guid,name in catalog.items():

    print()
    print("----------------")
    print(name)
    print("----------------")


    start = 0


    found = False


    while True:


        pos = data.find(
            guid,
            start
        )


        if pos == -1:
            break


        print(
            "GUID trouvé :",
            hex(pos)
        )


        #
        # Recherche matrice après GUID
        #

        for mpos in range(
            pos,
            min(pos+300,len(data)-64)
        ):


            matrix = read_matrix(
                mpos
            )


            if matrix is None:
                continue



            #
            # Matrice 4x4 :
            # dernière valeur = 1
            #

            if abs(matrix[15]-1)<0.01:


                x,y,z = matrix[12:15]


                if (
                    abs(x)<1000
                    and abs(y)<1000
                    and abs(z)<1000
                ):


                    print(
                        "Matrice :",
                        hex(mpos)
                    )


                    print(
                        "Position :",
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
                            for v in matrix[:12]
                        ]
                    )


                    found=True

                    break



        start = pos + 16



    if not found:

        print(
            "Instance non résolue"
        )



print()
print("Terminé")