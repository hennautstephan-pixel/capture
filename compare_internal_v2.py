from pathlib import Path


files = [
    "1 projecteur.bin",
    "1 projecteur_rotation.bin",
    "1 projecteur_deplacement.bin",
    "1 projecteur_dmx.bin",
]


base = Path("samples") / files[0]
base_data = base.read_bytes()


print("BASE :", files[0])
print("Taille :", len(base_data))


for name in files[1:]:

    path = Path("samples") / name
    data = path.read_bytes()

    print()
    print("==============================")
    print(name)
    print("==============================")

    diff = []

    for i,(a,b) in enumerate(zip(base_data,data)):

        if a != b:
            diff.append(i)


    print("Octets modifiés :", len(diff))


    if diff:

        print("Premier offset :", hex(diff[0]))
        print("Dernier offset :", hex(diff[-1]))


        # regroupement des zones

        zones=[]

        start=diff[0]
        last=diff[0]


        for d in diff[1:]:

            if d-last > 8:
                zones.append((start,last))
                start=d

            last=d


        zones.append((start,last))


        print()
        print("Zones modifiées :")


        for a,b in zones:

            print(
                hex(a),
                "-",
                hex(b),
                " taille:",
                b-a+1
            )


        # dump des octets changés

        print()
        print("Données :")

        for a,b in zones[:10]:

            print(
                hex(a),
                ":",
                data[a:b+1].hex()
            )