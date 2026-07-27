from dataclasses import dataclass, field

@dataclass(slots=True)
class Statistics:

    ascii_strings: int = 0
    utf16_strings: int = 0
    integers: int = 0
    floats: int = 0
    signatures: int = 0
    blocks: int = 0

    by_type: dict[str, int] = field(default_factory=dict)