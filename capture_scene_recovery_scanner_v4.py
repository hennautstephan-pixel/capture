from pathlib import Path
import struct
import json
import math


# Noms vus dans le catalogue Capture
CATALOG_NAMES = [
    "Ape Labs Neon Tube",
    "Nanlux",
    "Plancher",
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


def read_float(data, offset):

    try:
        return struct.unpack(
            "<f",
            data[offset:offset+4]
        )[0]

    except:
        return None



def valid(v):

    if v is None:
        return False

    if math.isnan(v):
        return False

    if math.isinf(v):
        return False

    if abs(v) > 10000:
        return False

    return True



def read_matrix(data, offset):

    values=[]

    for i in range(12):

        v=read_float(
            data,
            offset+i*4
        )

        if not valid(v):
            return None

        values.append(
            round(v,5)
        )

    return values



def find_catalog_name(data, offset):

    start=max(
        0,
        offset-800
    )

    end=min(
        len(data),
        offset+200
    )

    zone=data[start:end]


    found=[]


    for name in CATALOG_NAMES:

        if name.encode() in zone:

            found.append(name)


    if found:
        return found[-1]


    return "Unknown"



def find_guid_before(data, offset):

    start=max(
        0,
        offset-150
    )


    zone=data[start:offset]


    # recherche d'une signature GUID Capture
    pos=zone.rfind(
        b"\x01\x01\x01"
    )


    if pos==-1:

        return None


    real=start+pos


    return {
        "offset":hex(real),
        "guid":data[real:real+16].hex()
    }



def matrix_score(matrix):

    if matrix is None:
        return 0


    score=0


    # présence de valeurs typiques rotation

    small=0

    for v in matrix:

        if -1.2 <= v <= 1.2:

            small+=1


    if small>=8:

        score+=40



    # dernière colonne homogène souvent à 1

    if abs(matrix[3]-1)<0.01:

        score+=20



    return score



def scan(filename):


    path=Path(filename)

    data=path.read_bytes()


    print()
    print("==============================")
    print("CAPTURE RECOVERY SCANNER V4")
    print("==============================")

    print(
        "Fichier :",
        filename
    )

    print(
        "Taille :",
        len(data)
    )


    objects=[]


    print()
    print("Recherche matrices...")


    for offset in range(
        0,
        len(data)-48,
        4
    ):


        matrix=read_matrix(
            data,
            offset
        )


        score=matrix_score(
            matrix
        )


        if score < 50:

            continue



        guid=find_guid_before(
            data,
            offset
        )


        if guid is None:

            continue



        name=find_catalog_name(
            data,
            offset
        )


        obj={

            "name":name,

            "matrix_offset":hex(offset),

            "guid":guid,

            "matrix":matrix,

            "score":score

        }


        # éviter doublons

        duplicate=False

        for old in objects:

            if old["matrix_offset"]==obj["matrix_offset"]:

                duplicate=True


        if not duplicate:

            objects.append(obj)

            print()

            print(
                "[{}%]".format(score),
                name
            )

            print(
                "GUID",
                guid["offset"]
            )

            print(
                "Matrice",
                hex(offset)
            )



    return {

        "file":filename,

        "objects":objects

    }



if __name__=="__main__":


    import sys


    if len(sys.argv)<2:

        print(
            "Usage : python capture_scene_recovery_scanner_v4.py fichier.bin"
        )

        exit()



    result=scan(
        sys.argv[1]
    )


    print()

    print("==============================")

    print(
        "Objets trouvés :",
        len(result["objects"])
    )



    output=Path(
        sys.argv[1]
    ).with_suffix(
        ".recovery_v4.json"
    )


    output.write_text(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print(
        "Export :",
        output
    )