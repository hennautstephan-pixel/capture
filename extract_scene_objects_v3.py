from pathlib import Path
import struct
import json
import math


# ==========================
# CHOIX DU FICHIER
# ==========================

files = list(Path(".").glob("*.bin"))

if not files:
    raise Exception("Aucun fichier bin trouvé")

binfile = max(files, key=lambda x: x.stat().st_size)

print("Fichier utilisé :", binfile)
print("Taille :", binfile.stat().st_size)


data = binfile.read_bytes()


# ==========================
# GUID connus catalogue
# ==========================

catalog = {

"Nanlux":
bytes.fromhex(
"8ed0691bb3d24d0ba99c57303d3010ab"
),

"Ape Labs Neon Tube":
bytes.fromhex(
"5fb40e612ab74b58a00fc75047ec4bae"
)

}


# ==========================
# lecture float
# ==========================

def read_float(offset):

    try:
        return struct.unpack_from("<f", data, offset)[0]
    except:
        return None



# ==========================
# recherche GUID
# ==========================

def find_guid(guid):

    pos = []

    start = 0

    while True:

        p = data.find(guid,start)

        if p < 0:
            break

        pos.append(p)

        start = p+1

    return pos



# ==========================
# recherche matrice
# ==========================

def find_matrix(start):

    # on cherche autour de l'objet
    for off in range(start+16, start+600,4):

        vals=[]

        for i in range(12):
            v=read_float(off+i*4)
            if v is None:
                break
            vals.append(v)

        if len(vals)!=12:
            continue


        # rejet NaN
        if any(math.isnan(x) or math.isinf(x) for x in vals):
            continue


        # matrice plausible
        if (
            abs(vals[0])<=2 and
            abs(vals[5])<=2 and
            abs(vals[10])<=2
        ):

            return off, vals


    return None,None



# ==========================
# extraction
# ==========================


objects=[]


print()
print("========== SCENE ==========")


for name,guid in catalog.items():

    found=find_guid(guid)


    for instance in found:

        print()
        print("----------------")
        print(name)
        print("GUID :",hex(instance))


        mat_off,mat=find_matrix(instance)


        if mat_off is None:
            print("Pas de matrice")
            continue


        pos=[
            round(mat[9],4),
            round(mat[10],4),
            round(mat[11],4)
        ]


        print("Matrice :",hex(mat_off))
        print("Position :",pos)


        objects.append(
        {
            "name":name,
            "guid_offset":hex(instance),
            "matrix_offset":hex(mat_off),
            "position":pos,
            "matrix":mat
        })



# ==========================
# export
# ==========================

with open(
"capture_scene_full.json",
"w",
encoding="utf8"
) as f:

    json.dump(
        objects,
        f,
        indent=4,
        ensure_ascii=False
    )


print()
print("==========================")
print("Export terminé")
print("Objets :",len(objects))
print("Fichier : capture_scene_full.json")