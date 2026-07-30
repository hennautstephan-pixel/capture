from pathlib import Path
import json
import re
import struct


# Taille observée d'un bloc objet projecteur
OBJECT_SIZE = 14315


# Motif GUID Capture observé :
# 01 01 01 + 13 octets environ
GUID_PATTERN = re.compile(
    b"\x01\x01\x01.{13}"
)


def clean_ascii(data):

    text = ""

    for b in data:

        if 32 <= b <= 126:

            text += chr(b)

        else:

            text += " "


    return text



def find_names(data):

    """
    Recherche des noms ASCII présents
    dans le catalogue Capture
    """

    names=[]


    for match in re.finditer(
        b"[A-Za-z][A-Za-z0-9 _-]{3,40}",
        data
    ):

        value = match.group().decode(
            errors="ignore"
        ).strip()


        # éviter les faux positifs
        if len(value)>3:

            names.append(
                {
                    "name":value,
                    "offset":hex(match.start())
                }
            )


    return names



def find_guids(data):

    results=[]


    for match in GUID_PATTERN.finditer(data):

        offset=match.start()

        guid=match.group().hex()


        results.append(
            {
                "offset":hex(offset),
                "guid":guid
            }
        )


    return results



def nearby_name(data, offset):

    """
    Cherche un nom ASCII proche
    du GUID
    """

    start=max(
        0,
        offset-512
    )


    end=min(
        len(data),
        offset+512
    )


    zone=data[start:end]


    names=find_names(zone)


    if names:

        return names[-1]["name"]


    return "Unknown"



def read_position(data, offset):

    """
    Lecture position Capture connue
    """

    pos=offset+0x2BF8


    if pos+16 > len(data):

        return None


    return [

        round(
            struct.unpack(
                "<f",
                data[pos+i*4:pos+i*4+4]
            )[0],
            4
        )

        for i in range(4)

    ]



def scan(filename):


    path=Path(filename)

    data=path.read_bytes()


    print()
    print("==============================")
    print("CAPTURE RECOVERY SCANNER V2")
    print("==============================")

    print(
        "Fichier :",
        filename
    )

    print(
        "Taille :",
        len(data)
    )


    result={

        "file":filename,

        "size":len(data),

        "objects":[],

        "catalog_names":[]

    }



    print()
    print("Recherche GUID...")


    guids=find_guids(data)



    for g in guids:


        offset=int(
            g["offset"],
            16
        )


        obj={

            "guid_offset":g["offset"],

            "guid":g["guid"],

            "name":
                nearby_name(
                    data,
                    offset
                )

        }


        pos=read_position(
            data,
            offset
        )


        if pos:

            obj["position"]=pos



        result["objects"].append(
            obj
        )


        print(
            obj["name"],
            g["offset"]
        )



    result["catalog_names"]=find_names(
        data
    )



    return result



if __name__=="__main__":


    import sys


    if len(sys.argv)<2:

        print(
            "Usage : python capture_scene_recovery_scanner_v2.py fichier.bin"
        )

        exit()



    report=scan(
        sys.argv[1]
    )


    print()

    print(
        "Objets trouvés :",
        len(report["objects"])
    )


    output=Path(
        sys.argv[1]
    ).with_suffix(
        ".recovery_v2.json"
    )


    output.write_text(
        json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print(
        "Export :",
        output
    )