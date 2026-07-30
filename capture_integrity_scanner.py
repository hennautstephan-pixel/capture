from pathlib import Path
import struct
import json
import sys
import math


OBJECT_SIZE = 14315


# Cartographie actuelle issue des comparaisons
FIELDS = {

    "state_flag": {
        "offset": 0x2591,
        "size": 1,
        "type": "byte"
    },

    "position_main": {
        "offset": 0x2BF8,
        "size": 16,
        "type": "float4"
    },

    "geometry_parameters": {
        "offset": 0x2CFC,
        "size": 16,
        "type": "float4"
    },

    "rotation_axis_1": {
        "offset": 0x2D51,
        "size": 16,
        "type": "float4"
    },

    "rotation_axis_2": {
        "offset": 0x2D61,
        "size": 16,
        "type": "float4"
    },

    "position_secondary": {
        "offset": 0x2D71,
        "size": 16,
        "type": "float4"
    },

    "dmx_block": {
        "offset": 0x30B2,
        "size": 16,
        "type": "raw"
    }
}



def read_float4(data, offset):

    values=[]

    for i in range(4):

        pos = offset+i*4

        values.append(
            struct.unpack(
                "<f",
                data[pos:pos+4]
            )[0]
        )

    return values



def is_valid_float(value):

    if math.isnan(value):
        return False

    if math.isinf(value):
        return False

    if abs(value) > 100000:
        return False

    return True



def analyse_field(name, field, data):

    offset = field["offset"]

    result = {

        "status":"OK",

        "offset":hex(offset)

    }


    if offset + field["size"] > len(data):

        result["status"]="MISSING"

        return result



    if field["type"]=="float4":

        values = read_float4(
            data,
            offset
        )

        result["values"] = [
            round(v,6)
            for v in values
        ]


        invalid = [
            v for v in values
            if not is_valid_float(v)
        ]


        if invalid:

            result["status"]="INVALID"



    elif field["type"]=="byte":

        result["value"] = data[offset]



    elif field["type"]=="raw":

        block=data[
            offset:
            offset+field["size"]
        ]

        result["hex"]=block.hex()



    return result



def calculate_score(report):

    score=100


    for name,value in report["fields"].items():

        if value["status"]=="MISSING":

            score-=20


        elif value["status"]=="INVALID":

            score-=15



    if report["size"] != OBJECT_SIZE:

        score-=20



    return max(score,0)



def scan(filename):

    path=Path(filename)

    data=path.read_bytes()


    report={

        "file":str(path),

        "size":len(data),

        "fields":{}

    }



    for name,field in FIELDS.items():

        report["fields"][name]=analyse_field(
            name,
            field,
            data
        )



    report["recovery_score"]=calculate_score(
        report
    )


    return report



if __name__=="__main__":


    if len(sys.argv)<2:

        print(
            "Usage : python capture_integrity_scanner.py fichier.bin"
        )

        sys.exit(1)



    result=scan(
        sys.argv[1]
    )


    print()
    print("==============================")
    print("CAPTURE INTEGRITY SCANNER")
    print("==============================")


    print(
        json.dumps(
            result,
            indent=4
        )
    )


    output=Path(
        sys.argv[1]
    ).with_suffix(
        ".integrity.json"
    )


    output.write_text(
        json.dumps(
            result,
            indent=4
        ),
        encoding="utf-8"
    )


    print()
    print("Export :",output)