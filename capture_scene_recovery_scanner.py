from pathlib import Path
import json
import struct


OBJECT_SIZE = 14315


# Objets connus trouvés dans les fichiers Capture
KNOWN_OBJECTS = {

    "Ape Labs Neon Tube":
        bytes.fromhex(
            "5fb40e612ab74b58a00fc75047ec4bae"
        ),

    "Nanlux":
        bytes.fromhex(
            "8ed0691bb3d24d0ba99c57303d3010ab"
        )
}



# Champs contrôlés
FIELDS = {

    "state_flag": 0x2591,

    "position_main": 0x2BF8,

    "geometry_parameters": 0x2CFC,

    "rotation_axis_1": 0x2D51,

    "rotation_axis_2": 0x2D61,

    "position_secondary": 0x2D71,

    "dmx_block": 0x30B2

}



def read_float4(data, offset):

    values=[]

    try:

        for i in range(4):

            values.append(
                round(
                    struct.unpack(
                        "<f",
                        data[offset+i*4:
                             offset+i*4+4]
                    )[0],
                    6
                )
            )

    except:

        pass


    return values



def check_object(block):

    report={}


    report["size"] = len(block)


    if len(block) != OBJECT_SIZE:

        report["size_status"]="invalid"

    else:

        report["size_status"]="OK"



    report["fields"]={}



    # Flag

    if len(block)>0x2591:

        report["fields"]["state_flag"] = block[0x2591]



    # Transformations

    for name,offset in FIELDS.items():

        if name in [
            "state_flag",
            "dmx_block"
        ]:

            continue


        if offset+16 <= len(block):

            report["fields"][name]=read_float4(
                block,
                offset
            )



    # DMX

    if 0x30B2+16 <= len(block):

        dmx=block[
            0x30B2:
            0x30B2+16
        ]

        report["fields"]["dmx_block"]={

            "hex":dmx.hex(),

            "active":
                dmx != bytes(16)

        }



    # Score

    score=100


    if report["size_status"]!="OK":

        score-=30


    for key,value in report["fields"].items():

        if isinstance(value,list):

            for v in value:

                if abs(v)>100000:

                    score-=10



    report["recovery_score"]=max(score,0)


    return report



def scan_file(filename):


    path=Path(filename)

    data=path.read_bytes()


    print()
    print("==============================")
    print("CAPTURE RECOVERY SCANNER")
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

        "objects":[]

    }



    print()
    print("Recherche objets...")



    for name,guid in KNOWN_OBJECTS.items():


        start=0


        while True:


            pos=data.find(
                guid,
                start
            )


            if pos==-1:

                break



            print()

            print(
                "Objet trouvé :",
                name
            )

            print(
                "GUID offset :",
                hex(pos)
            )



            # tentative extraction

            begin=pos-0x80


            if begin<0:

                begin=pos



            end=begin+OBJECT_SIZE



            if end<=len(data):

                block=data[
                    begin:end
                ]


                analysis=check_object(
                    block
                )


                obj={

                    "name":name,

                    "guid_offset":hex(pos),

                    "object_offset":hex(begin),

                    "analysis":analysis

                }


                result["objects"].append(obj)



            start=pos+1



    return result



if __name__=="__main__":


    import sys


    if len(sys.argv)<2:


        print(
            "Usage : python capture_scene_recovery_scanner.py fichier.bin"
        )


        exit()



    report=scan_file(
        sys.argv[1]
    )



    print()
    print("==============================")
    print(
        "Objets récupérés :",
        len(report["objects"])
    )



    output=Path(
        sys.argv[1]
    ).with_suffix(
        ".recovery.json"
    )


    output.write_text(
        json.dumps(
            report,
            indent=4
        ),
        encoding="utf-8"
    )


    print(
        "Export :",
        output
    )