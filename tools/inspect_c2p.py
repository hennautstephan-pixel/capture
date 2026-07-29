from __future__ import annotations

import argparse
import zlib
from pathlib import Path


def extract_ascii(data: bytes, minimum: int = 4) -> list[str]:
    strings: list[str] = []
    current = bytearray()

    for b in data:
        if 32 <= b <= 126:
            current.append(b)
        else:
            if len(current) >= minimum:
                strings.append(current.decode("ascii", errors="replace"))
            current.clear()

    if len(current) >= minimum:
        strings.append(current.decode("ascii", errors="replace"))

    return strings


def find_zlib_streams(data: bytes) -> list[int]:
    headers = {
        (0x78, 0x01),
        (0x78, 0x5E),
        (0x78, 0x9C),
        (0x78, 0xDA),
    }

    offsets = []

    for i in range(len(data) - 1):
        if (data[i], data[i + 1]) in headers:
            offsets.append(i)

    return offsets


def analyse_file(filename: Path, output_dir: Path) -> None:

    data = filename.read_bytes()

    print("=" * 70)
    print("Capture C2P Inspector")
    print("=" * 70)
    print()

    print(f"File : {filename}")
    print(f"Size : {len(data)} bytes")
    print()

    print("First 64 bytes")
    print("-" * 70)
    print(data[:64].hex(" "))
    print()

    print("ASCII strings")
    print("-" * 70)

    strings = extract_ascii(data)

    if strings:
        for s in strings:
            print(s)
    else:
        print("(none)")

    print()

    print("ZLIB streams")
    print("-" * 70)

    offsets = find_zlib_streams(data)

    if not offsets:
        print("No zlib stream found.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    for index, offset in enumerate(offsets):

        print(f"Offset : {offset}")

        try:
            payload = zlib.decompress(data[offset:])

            outfile = output_dir / f"zlib_{index:03d}.bin"
            outfile.write_bytes(payload)

            print(f"  Decompressed : {len(payload)} bytes")
            print(f"  Saved        : {outfile}")

            print()

            print("First 256 bytes")

            try:
                print(payload[:256].decode("utf-8"))
            except UnicodeDecodeError:
                print(payload[:256].hex(" "))

            print()

        except Exception as exc:
            print(f"  ERROR : {exc}")
            print()


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Inspect Capture C2P files."
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Capture .c2p file",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output"),
        help="Output directory",
    )

    args = parser.parse_args()

    analyse_file(args.file, args.output)


if __name__ == "__main__":
    main()