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


GUID_SIZE = 16
MATRIX_OFFSET = 0x12


def f32(data, offset):

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

    return abs(v) < 100000



def read_matrix(data, offset):

    values=[]

    for i in range(12):

        v=f32(
            data,
            offset+i*4
        )

        if not valid(v):
            return None

        values.append(v)

    return values



def matrix_is_real(matrix):

    if matrix is None:
        return False


    # rotation 3x3
    rot=matrix[:9]


    good=0

    for v in rot:

        if -1.5 <= v <= 1.5:

            good+=1


    if good < 7:

        return False


    return True



def position(matrix):

    if matrix is None:

        return None


    # translation dans la matrice Capture
    p=[
        matrix[9],
        matrix[10],
        matrix[11]
    ]


    if any(
        abs(v)>500
        for v in p
    ):

        return None


    return [
        round(v,4)
        for v in p
    ]



def find_name(data, offset):

    zone=data[
        max(0,offset-800):
        offset+400
    ]


    found=[]


    for name in CATALOG_NAMES:

        if name.encode() in zone:

            found.append(name)


    if found:

        return found[-1]


    return "Unknown"



def get_guid(data, matrix_offset):


    guid_offset = (
        matrix_offset
        -
        MATRIX_OFFSET
    )


    if guid_offset < 0:

        return None



    guid=data[
        guid_offset:
        guid_offset+GUID_SIZE
    ]


    if len(guid)!=16:

        return None



    return {

        "offset":guid_offset,

        "hex":guid.hex()

    }



def has_context(data, guid_offset):

    zone=data[
        max(0,guid_offset-300):
        guid_offset+300
    ]


    score=0


    for name in CATALOG_NAMES:

        if name.encode() in zone:

            score+=30


    # présence d'un bloc Capture
    if b"\x01\x01\x01" in zone:

        score+=20


    return score



def scan(filename):


    data=Path(filename).read_bytes()


    print()
    print("==============================")
    print("CAPTURE RECOVERY SCANNER V6")
    print("==============================")


    objects=[]

    used=[]



    # on cherche uniquement les zones qui ressemblent
    # aux instances déjà identifiées
    for pos in range(
        0,
        len(data)-64,
        4
    ):


        matrix=read_matrix(
            data,
            pos
        )


        if not matrix_is_real(matrix):

            continue



        guid=get_guid(
            data,
            pos
        )


        if guid is None:

            continue



        if guid["offset"] in used:

            continue



        context=has_context(
            data,
            guid["offset"]
        )


        if context < 20:

            continue



        p=position(matrix)


        if p is None:

            continue



        used.append(
            guid["offset"]
        )


        obj={

            "name":
                find_name(
                    data,
                    guid["offset"]
                ),

            "guid":

                {
                    "offset":
                        hex(guid["offset"]),

                    "value":
                        guid["hex"]
                },


            "matrix":
                hex(pos),


            "position":
                p,


            "score":
                context

        }


        objects.append(obj)


        print()
        print(obj["name"])
        print(
            "GUID",
            obj["guid"]["offset"]
        )
        print(
            "Matrix",
            obj["matrix"]
        )
        print(
            "Position",
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
            "usage: python capture_scene_recovery_scanner_v6.py fichier.bin"
        )

        exit()



    result=scan(
        sys.argv[1]
    )


    out=Path(sys.argv[1]).with_suffix(
        ".recovery_v6.json"
    )


    out.write_text(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print()
    print("==============================")
    print(
        "Objets récupérés :",
        len(result["objects"])
    )
    print(
        "Export :",
        out
    )