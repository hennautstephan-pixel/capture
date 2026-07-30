from pathlib import Path
import struct


data = Path(
    "capture_block_full.bin"
).read_bytes()


# GUID connus catalogue

catalog = {

    "Ape Labs Neon Tube":
    bytes.fromhex(
        "fa83a06db8279346a84423293f02c38f"
    ),

    "Nanlux":
    bytes.fromhex(
        "f2dbfd8a6f6d4e6cbec6750a9f245b21"
    ),

    "Mandarine":
    bytes.fromhex(
        "a2b5b3a11ce049789bc20691580f0a10"
    )

}



print()
print("========== LIENS CATALOGUE / INSTANCE ==========")



for name,guid in catalog.items():


    print()
    print("----",name,"----")


    positions=[]

    start=0

    while True:

        p=data.find(
            guid,
            start
        )

        if p==-1:
            break

        positions.append(p)

        start=p+1



    for p in positions:

        print(
            "Catalogue GUID :",
            hex(p)
        )


        # rechercher les GUID proches après

        zone=data[
            p:
            p+512
        ]


        for off in range(
            0,
            len(zone)-16
        ):


            candidate=zone[
                off:
                off+16
            ]


            # ignorer le même GUID

            if candidate==guid:
                continue


            if candidate.count(0)<8:

                print(
                    "  possible instance",
                    hex(p+off),
                    candidate.hex()
                )



print()
print("FIN")