from pathlib import Path
import re


data = Path("capture_block_full.bin").read_bytes()


for m in re.finditer(rb'[\x20-\x7E]{4,30}', data):

    pos = m.start()
    text = m.group().decode("ascii", errors="ignore")

    if text in [
        "Ape Labs Neon Tube",
        "Plancher",
        "Nanlux",
        "Plancher SKP",
        "Piano",
        "Mandarine",
        "Ampoule",
        "Pendrillons",
        "Trussxxx",
        "Table",
        "Perche",
        "PC face"
    ]:

        print("\n",hex(pos),text)

        print(
            data[pos-24:pos+80].hex(" ")
        )