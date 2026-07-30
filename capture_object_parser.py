from pathlib import Path
import struct
import json
import sys


# Taille observée des objets projecteurs décompressés
OBJECT_SIZE = 14315


# Champs actuellement identifiés
# Les champs DMX ne sont pas encore décodés :
# ils sont conservés en brut.

FIELDS = {

    "position_main": {
        "type": "float",
        "offset": 0x2BF8,
        "count": 4
    },

    "optical_parameters": {
        "type": "float",
        "offset": 0x2CFC,
        "count": 4
    },

    "rotation_axis_1": {
        "type": "float",
        "offset": 0x2D51,
        "count": 4
    },

    "rotation_axis_2": {
        "type": "float",
        "offset": 0x2D61,
        "count": 4
    },

    "position_secondary": {
        "type": "float",
        "offset": 0x2D71,
        "count": 4
    },

    "dmx_block": {
        "type": "raw",
        "offset": 0x30B2,
        "size": 16
    }
}



def read_floats(data, offset, count):

    values = []

    for i in range(count):

        pos = offset + i * 4

        if pos + 4 <= len(data):

            value = struct.unpack(
                "<f",
                data[pos:pos+4]
            )[0]

            values.append(
                round(value, 6)
            )

    return values



def read_raw(data, offset, size):

    if offset + size <= len(data):

        return data[offset:offset+size].hex()

    return None



def read_uints(data, offset, size):

    values = []

    block = data[offset:offset+size]

    for i in range(0, len(block)-3, 4):

        values.append(
            struct.unpack(
                "<I",
                block[i:i+4]
            )[0]
        )

    return values



def analyse_integrity(data):

    score = 100
    errors = []


    if len(data) != OBJECT_SIZE:

        score -= 20

        errors.append(
            f"Taille inattendue : {len(data)} octets"
        )


    for name,field in FIELDS.items():

        if field["offset"] >= len(data):

            score -= 5

            errors.append(
                f"Champ absent : {name}"
            )


    return {

        "score": max(score,0),

        "errors": errors

    }



def parse_object(filename):

    path = Path(filename)

    data = path.read_bytes()


    result = {

        "file": str(path),

        "size": len(data),

        "fields": {}

    }



    for name,field in FIELDS.items():

        if field["type"] == "float":

            result["fields"][name] = read_floats(
                data,
                field["offset"],
                field["count"]
            )


        elif field["type"] == "raw":

            result["fields"][name] = {

                "hex": read_raw(
                    data,
                    field["offset"],
                    field["size"]
                ),

                "uint32": read_uints(
                    data,
                    field["offset"],
                    field["size"]
                )

            }



    result["integrity"] = analyse_integrity(data)


    return result



if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage : python capture_object_parser.py fichier.bin"
        )

        sys.exit(1)



    result = parse_object(sys.argv[1])


    print()
    print("==============================")
    print("CAPTURE OBJECT PARSER")
    print("==============================")

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )


    output = Path(sys.argv[1]).with_suffix(".json")


    output.write_text(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print()
    print("Export :", output)