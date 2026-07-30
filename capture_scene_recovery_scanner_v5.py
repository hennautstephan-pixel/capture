from pathlib import Path
import struct
import json
import math


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


MATRIX_OFFSET_FROM_GUID = 0x12


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



def read_matrix(data, offset):

    values=[]

    for i in range(12):

        v=read_float(
            data,
            offset+i*4
        )

        if not valid_float(v):
            return None

        values.append(v)


    return values



def read_position(matrix):

    if matrix is None:
        return None


    return [
        round(matrix[9],4),
        round(matrix[10],4),
        round(matrix[11],4)
    ]



def find_name(data, offset):

    zone=data[
        max(0,offset-600):
        offset+300
    ]


    found=[]


    for name in CATALOG_NAMES:

        if name.encode() in zone:

            found.append(name)


    if found:

        return found[-1]


    return "Unknown"



def find_guid_from_matrix(data, matrix_offset):


    guid_offset = (
        matrix_offset
        -
        MATRIX_OFFSET_FROM_GUID
    )


    if guid_offset < 0:

        return None



    guid=data[
        guid_offset:
        guid_offset+16
    ]



    if len(guid)!=16:

        return None



    return {

        "offset":hex(guid_offset),

        "guid":guid.hex()

    }



def scan(filename):


    path=Path(filename)

    data=path.read_bytes()



    print()
    print("==============================")
    print("CAPTURE RECOVERY SCANNER V5")
    print("==============================")

    print(
        "Fichier :",
        filename
    )


    objects=[]

    used_guid=[]



    print()
    print("Recherche matrices Capture...")



    for matrix_offset in range(
        0,
        len(data)-48,
        4
    ):


        matrix=read_matrix(
            data,
            matrix_offset
        )


        if matrix is None:

            continue



        # test matrice plausible

        small=sum(
            1 for x in matrix
            if -1.2 < x < 1.2
        )


        if small < 8:

            continue



        guid=find_guid_from_matrix(
            data,
            matrix_offset
        )


        if guid is None:

            continue



        if guid["offset"] in used_guid:

            continue



        used_guid.append(
            guid["offset"]
        )



        name=find_name(
            data,
            int(
                guid["offset"],
                16
            )
        )



        obj={

            "name":name,

            "guid":guid,

            "matrix_offset":hex(matrix_offset),

            "position":
                read_position(matrix)

        }


        objects.append(obj)



        print()

        print(
            name
        )

        print(
            "GUID :",
            guid["offset"]
        )

        print(
            "Matrice :",
            hex(matrix_offset)
        )

        print(
            "Position :",
            obj["position"]
        )



    return {

        "file":filename,

        "objects":objects

    }



if __name__=="__main__":


    import sys


    if len(sys.argv)<2:

        print(
            "Usage : python capture_scene_recovery_scanner_v5.py fichier.bin"
        )

        exit()



    result=scan(
        sys.argv[1]
    )


    print()

    print("==============================")

    print(
        "Objets récupérés :",
        len(result["objects"])
    )



    output=Path(
        sys.argv[1]
    ).with_suffix(
        ".recovery_v5.json"
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