from pathlib import Path
import re
import struct
import json


# ======================================
# Chargement fichier Capture extrait
# ======================================

data = Path(
    "capture_block_full.bin"
).read_bytes()


print()
print("Fichier :", "capture_block_full.bin")
print("Taille :", len(data))


# ======================================
# Signatures recherchées
# ======================================

keywords = [
    b"Fixture",
    b"Universe",
    b"Channel",
    b"Evoke 600C",
    b"Nanlux",
    b"Mandarine",
    b"DMX",
    b"Address",
    b"Reference",
]


# ======================================
# Recherche chaînes
# ======================================

hits = []


print()
print("========== SIGNATURES ==========")


for k in keywords:

    pos = [
        m.start()
        for m in re.finditer(
            re.escape(k),
            data
        )
    ]

    print(
        k.decode(),
        ":",
        len(pos)
    )


    for p in pos:
        hits.append(
            (
                p,
                k.decode()
            )
        )



# ======================================
# Dump contexte
# ======================================

results=[]


print()
print("========== CONTEXTES FIXTURES ==========")



for pos,name in hits:


    # uniquement zones intéressantes

    block = data[
        max(0,pos-150):
        pos+300
    ]


    print()
    print("-----------------------------")
    print(
        name,
        hex(pos)
    )


    txt = block.decode(
        "utf8",
        errors="ignore"
    )


    print(
        txt[:300]
        .replace("\n"," ")
    )


    results.append(
        {
            "keyword":name,
            "offset":hex(pos),
            "hex":
                block.hex()
        }
    )



# ======================================
# Export
# ======================================

with open(
    "fixtures_context.json",
    "w",
    encoding="utf8"
) as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )


print()
print(
"Export : fixtures_context.json"
)