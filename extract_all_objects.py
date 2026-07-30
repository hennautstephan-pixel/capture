from pathlib import Path
import struct
import math
import re


data = Path("capture_block_full.bin").read_bytes()



# ---------------------------------
# Vérification matrice Capture
# ---------------------------------

def is_matrix(vals):

    if abs(vals[15]-1.0) > 0.001:
        return False


    # éviter identité
    if (
        abs(vals[0]-1)<0.001 and
        abs(vals[5]-1)<0.001 and
        abs(vals[10]-1)<0.001 and
        abs(vals[15]-1)<0.001
    ):
        pass


    x,y,z = vals[12],vals[13],vals[14]


    if abs(x)>1000 or abs(y)>1000 or abs(z)>1000:
        return False


    # vérifier axes rotation

    for a,b,c in [
        (0,1,2),
        (4,5,6),
        (8,9,10)
    ]:

        l = math.sqrt(
            vals[a]**2+
            vals[b]**2+
            vals[c]**2
        )

        if abs(l-1)>0.05:
            return False


    return True



# ---------------------------------
# Recherche noms dans le fichier
# ---------------------------------

names=[]


for m in re.finditer(
    rb'[A-Za-z][A-Za-z0-9 \-]{3,40}',
    data
):

    try:
        s=m.group().decode("utf-8")

    except:
        continue


    if s in [
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
    ]:

        names.append(
            (
                s,
                m.start()
            )
        )



print("Objets trouvés :",len(names))



# ---------------------------------
# Extraction matrices autour du nom
# ---------------------------------

for name,pos in names:


    print("\n====================")
    print(name)
    print("Offset nom :",hex(pos))


    start=max(0,pos-600)
    end=min(len(data),pos+600)


    matrices=[]


    for p in range(start,end):

        if p+64>len(data):
            continue


        try:

            vals=struct.unpack(
                "<16f",
                data[p:p+64]
            )

        except:

            continue


        if is_matrix(vals):

            matrices.append(
                (
                    p,
                    vals[12],
                    vals[13],
                    vals[14],
                    vals
                )
            )


    # filtrage doublons

    clean=[]

    for m in matrices:

        if not clean or abs(m[0]-clean[-1][0])>16:
            clean.append(m)



    for p,x,y,z,mat in clean[:3]:

        print(
            "Matrice",
            hex(p)
        )

        print(
            "XYZ =",
            round(x,3),
            round(y,3),
            round(z,3)
        )