from pathlib import Path
import struct
import re


# ==================================================
# Chargement
# ==================================================

data = Path("capture_block_full.bin").read_bytes()


# ==================================================
# Objets connus
# ==================================================

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
    "PC face",
]


# ==================================================
# Fonctions
# ==================================================

def is_guid(b):

    if len(b) != 16:
        return False

    ascii_count = sum(
        32 <= x <= 126
        for x in b
    )

    zero_count = b.count(0)

    # élimine les faux blocs
    if ascii_count > 5:
        return False

    if zero_count > 5:
        return False

    return True



def read_matrix(pos):

    try:

        return struct.unpack(
            "<16f",
            data[pos:pos+64]
        )

    except:

        return None



def find_matrix(start):

    for p in range(
        start,
        min(start+500,len(data)-64)
    ):

        m = read_matrix(p)

        if not m:
            continue


        # matrice 4x4 Capture
        if abs(m[15]-1.0)<0.01:

            x,y,z=m[12:15]


            if (
                abs(x)<1000
                and abs(y)<1000
                and abs(z)<1000
            ):

                return p,m


    return None,None



# ==================================================
# Extraction catalogue
# ==================================================

print()
print("========== CATALOGUE ==========")


catalog=[]


for name in objects:


    pos=data.find(
        name.encode()
    )


    if pos==-1:
        continue


    zone=data[
        pos+len(name):
        pos+len(name)+300
    ]


    found=[]


    for i in range(len(zone)-16):

        g=zone[i:i+16]


        if is_guid(g):

            found.append(g)



    if found:

        guid=found[-1]

        catalog.append(
            (name,guid)
        )


        print(
            name,
            guid.hex()
        )



print()
print(
    "Catalogue trouvé :",
    len(catalog)
)



# ==================================================
# Recherche instances
# ==================================================

print()
print("========== INSTANCES ==========")



for name,catalog_guid in catalog:


    print()
    print("====================")
    print(name)
    print("====================")


    positions=[]


    # chercher toutes occurrences du GUID
    start=0


    while True:


        p=data.find(
            catalog_guid,
            start
        )


        if p==-1:
            break


        positions.append(p)

        start=p+1



    print(
        "GUID catalogue occurrences:",
        [hex(x) for x in positions]
    )


    # recherche d'un GUID différent proche
    instance_guid=None


    for p in positions:


        zone=data[
            p-200:
            p+300
        ]


        for i in range(len(zone)-16):

            g=zone[i:i+16]


            if (
                is_guid(g)
                and g != catalog_guid
            ):

                instance_guid=g
                break


        if instance_guid:
            break



    if instance_guid:


        print(
            "GUID instance:",
            instance_guid.hex()
        )


        ip=data.find(
            instance_guid
        )


        mp,matrix=find_matrix(ip)


        if matrix:


            print(
                "Matrice:",
                hex(mp)
            )


            print(
                "Position:",
                round(matrix[12],3),
                round(matrix[13],3),
                round(matrix[14],3)
            )


            print(
                "Rotation:"
            )


            print(
                [
                    round(x,4)
                    for x in matrix[:12]
                ]
            )


        else:

            print(
                "Matrice non trouvée"
            )


    else:

        print(
            "GUID instance non trouvé"
        )


print()
print("FIN")