from pathlib import Path


base = Path("samples/1 projecteur.bin").read_bytes()
rot = Path("samples/1 projecteur_rotation.bin").read_bytes()


print("========== NOUVELLES STRUCTURES ==========")


diff=[]

for i,(a,b) in enumerate(zip(base,rot)):
    if a != b:
        diff.append(i)


for d in diff:
    if d > 0x3000:
        print(hex(d), hex(base[d]), "->", hex(rot[d]))