from pathlib import Path


base = Path("samples/1 projecteur.bin").read_bytes()
dmx = Path("samples/1 projecteur_dmx.bin").read_bytes()


print("========== DMX DIFFERENCES ==========")


diff=[]

for i,(a,b) in enumerate(zip(base,dmx)):

    if a != b:
        diff.append(i)


for d in diff:

    if d >= 0x2500:

        print(
            hex(d),
            hex(base[d]),
            "->",
            hex(dmx[d])
        )


print()
print("Total différences :",len(diff))