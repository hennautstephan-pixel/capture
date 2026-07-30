from pathlib import Path
import json
import struct
import re
import math


# Taille observée d'un objet décompressé
OBJECT_SIZE = 14315


# Noms connus trouvés dans le catalogue Capture
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



def valid_float(v):

    if v is None:
        return False

    if math.isnan(v):
        return False

    if math.isinf(v):
        return False

    if abs(v) > 100000:
        return False

    return True



def find_catalog_name(data, offset):

    start=max(
        0,
        offset-600
    )

    end=min(
        len(data),
        offset+600
    )


    zone=data[start:end]


    found=[]


    for name in CATALOG_NAMES:

        if name.encode() in zone:

            found.append(name)


    if found:

        return found[-1]


    return "Unknown"



def find_candidate_guids(data):

    results=[]


    # Capture utilise beaucoup de séquences 010101
    # mais on impose des critères supplémentaires

    for m in re.finditer(
        b"\x01\x01\x01",
        data
    ):

        offset=m.start()


        if offset < 0x1000:

            continue


        block=data[offset:offset+64]


        # recherche d'une zone qui ressemble à un GUID

        if len(block)>=20:


            results.append(offset)



    return results



def analyse_candidate(data, offset):


    score=0


    name=find_catalog_name(
        data,
        offset
    )


    if name!="Unknown":

        score+=30



    # tentative position Capture
    # le GUID est proche de la matrice

    matrix_offset=offset+0x12


    x=read_float(
        data,
        matrix_offset
    )

    y=read_float(
        data,
        matrix_offset+4
    )

    z=read_float(
        data,
        matrix_offset+8
    )


    position=None


    if all(
        valid_float(v)
        for v in [x,y,z]
    ):


        if (
            -1000 < x < 1000 and
            -1000 < y < 1000 and
            -1000 < z < 1000
        ):

            score+=30

            position=[
                round(x,4),
                round(y,4),
                round(z,4)
            ]



    # présence d'une structure Capture proche

    zone=data[
        offset:
        offset+128
    ]


    if b"\x01\x01\x01" in zone:

        score+=20



    if score>=50:

        valid=True

    else:

        valid=False



    return {

        "name":name,

        "offset":hex(offset),

        "score":score,

        "valid":valid,

        "position":position

    }



def scan(filename):


    path=Path(filename)

    data=path.read_bytes()


    print()
    print("==============================")
    print("CAPTURE RECOVERY SCANNER V3")
    print("==============================")


    print(
        "Fichier :",
        filename
    )

    print(
        "Taille :",
        len(data)
    )


    candidates=find_candidate_guids(
        data
    )


    print()
    print(
        "GUID candidats :",
        len(candidates)
    )


    objects=[]


    rejected=0


    for offset in candidates:


        result=analyse_candidate(
            data,
            offset
        )


        if result["valid"]:

            objects.append(
                result
            )

            print()

            print(
                "[{}%]".format(
                    result["score"]
                ),
                result["name"],
                result["offset"]
            )

        else:

            rejected+=1



    return {

        "file":filename,

        "objects":objects,

        "rejected":rejected

    }



if __name__=="__main__":


    import sys


    if len(sys.argv)<2:

        print(
            "Usage : python capture_scene_recovery_scanner_v3.py fichier.bin"
        )

        exit()



    report=scan(
        sys.argv[1]
    )


    print()

    print("==============================")

    print(
        "Objets récupérés :",
        len(report["objects"])
    )

    print(
        "Faux positifs supprimés :",
        report["rejected"]
    )


    output=Path(
        sys.argv[1]
    ).with_suffix(
        ".recovery_v3.json"
    )


    output.write_text(
        json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print()

    print(
        "Export :",
        output
    )