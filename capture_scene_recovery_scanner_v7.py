from pathlib import Path
import struct
import json
import math


# Structures validées depuis :
# 1 projecteur.bin
# 1 projecteur_dmx.bin

OFFSETS = {

    "state_flag": 0x2591,

    "position_main": 0x2BF8,

    "optics": 0x2CFC,

    "rotation1": 0x2D51,

    "rotation2": 0x2D61,

    "position_secondary": 0x2D71,

    "dmx": 0x30B2

}


CATALOG = [

    "Nanlux",

    "Ape Labs",

    "Neon Tube",

    "Evoke",

    "Mandarine"

]



def read_float(data,offset):

    try:

        return struct.unpack(
            "<f",
            data[offset:offset+4]
        )[0]

    except:

        return None



def floats(data,offset,count):

    result=[]

    for i in range(count):

        v=read_float(
            data,
            offset+i*4
        )

        if v is None:

            return None

        result.append(
            round(v,6)
        )

    return result



def valid_values(values):

    if values is None:

        return False


    for v in values:

        if math.isnan(v):

            return False

        if math.isinf(v):

            return False


        if abs(v)>10000:

            return False


    return True



def find_name(data,offset):

    zone=data[
        max(0,offset-1000):
        offset+1000
    ]


    names=[]


    for n in CATALOG:

        if n.encode() in zone:

            names.append(n)


    if names:

        return " ".join(names)


    return "Unknown"



def analyse_instance(data,guid_offset):


    base=guid_offset


    matrix_offset = (
        base + 0x12
    )


    # position principale
    pos=floats(
        data,
        base + (
            OFFSETS["position_main"]
            -
            0x2591
        ),
        4
    )


    optics=floats(
        data,
        base + (
            OFFSETS["optics"]
            -
            0x2591
        ),
        4
    )


    rot1=floats(
        data,
        base + (
            OFFSETS["rotation1"]
            -
            0x2591
        ),
        4
    )


    rot2=floats(
        data,
        base + (
            OFFSETS["rotation2"]
            -
            0x2591
        ),
        4
    )


    secondary=floats(
        data,
        base + (
            OFFSETS["position_secondary"]
            -
            0x2591
        ),
        4
    )


    dmx=data[
        base + (
            OFFSETS["dmx"]
            -
            0x2591
        ):
        base + (
            OFFSETS["dmx"]
            -
            0x2591
        ) + 16
    ]


    score=0


    if valid_values(pos):

        score+=20


    if valid_values(optics):

        # paramètres optiques réalistes

        if (
            0 < optics[0] < 100
            and
            0 < optics[1] < 100
        ):

            score+=30



    if valid_values(rot1):

        score+=10


    if valid_values(rot2):

        score+=10


    if valid_values(secondary):

        score+=10



    if dmx != bytes(16):

        score+=20



    if score < 70:

        return None



    return {

        "guid_offset":hex(guid_offset),

        "matrix_offset":hex(matrix_offset),

        "name":
            find_name(
                data,
                guid_offset
            ),

        "position_main":pos,

        "optics":optics,

        "rotation_axis_1":rot1,

        "rotation_axis_2":rot2,

        "position_secondary":secondary,

        "dmx":
            dmx.hex(),

        "confidence":score

    }



def scan(filename):


    data=Path(filename).read_bytes()


    print()
    print("==============================")
    print("CAPTURE RECOVERY SCANNER V7")
    print("==============================")

    print(
        "Taille :",
        len(data)
    )


    objects=[]


    # recherche des GUID possibles
    # basé sur les zones déjà identifiées

    for offset in range(
        0,
        len(data)-0x3100,
        1
    ):


        # structure GUID Capture
        block=data[offset:offset+16]


        if len(block)!=16:

            continue



        # recherche d'une signature proche
        near=data[
            offset:
            offset+64
        ]


        if b"\x01\x01\x01" not in near:

            continue



        obj=analyse_instance(
            data,
            offset
        )


        if obj:


            # éviter doublons

            exists=False

            for old in objects:

                if old["guid_offset"]==obj["guid_offset"]:

                    exists=True


            if not exists:

                objects.append(obj)


                print()

                print(
                    obj["name"]
                )

                print(
                    "GUID",
                    obj["guid_offset"]
                )

                print(
                    "Position",
                    obj["position_main"]
                )

                print(
                    "Score",
                    obj["confidence"]
                )



    return objects



if __name__=="__main__":


    import sys


    if len(sys.argv)<2:

        print(
            "Usage : python capture_scene_recovery_scanner_v7.py fichier.bin"
        )

        exit()


    filename=sys.argv[1]


    objects=scan(
        filename
    )


    report={

        "file":filename,

        "objects":objects,

        "count":len(objects)

    }


    output=Path(filename).with_suffix(
        ".recovery_v7.json"
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

    print("==============================")

    print(
        "Objets récupérés :",
        len(objects)
    )

    print(
        "Export :",
        output
    )