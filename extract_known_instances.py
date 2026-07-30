from pathlib import Path
import struct


data = Path("capture_block_full.bin").read_bytes()



objects = {

"Ape Labs Neon Tube":
{
"catalog":"fa83a06db8279346a84423293f02c38f",
"instance":"5fb40e612ab74b58a00fc75047ec4bae"
},


"Nanlux":
{
"catalog":"f2dbfd8a6f6d4e6cbeC6750a9f245b21".lower(),
"instance":"8ed0691bb3d24d0ba99c57303d3010ab"
}

}



def matrix(pos):

    return struct.unpack(
        "<16f",
        data[pos:pos+64]
    )



for name,obj in objects.items():

    print()
    print("================")
    print(name)
    print("================")


    guid=bytes.fromhex(
        obj["instance"]
    )


    p=data.find(guid)


    print(
        "Instance GUID:",
        hex(p)
    )


    if p==-1:
        continue


    # recherche matrice après GUID

    for x in range(
        p,
        p+300
    ):

        try:

            m=matrix(x)

        except:

            continue


        if abs(m[15]-1)<0.01:


            print(
                "Matrice:",
                hex(x)
            )


            print(
                "XYZ:",
                round(m[12],3),
                round(m[13],3),
                round(m[14],3)
            )


            print(
                "Rotation:"
            )

            print(
                [
                round(v,4)
                for v in m[:12]
                ]
            )

            break