"""
Tests for capture_recovery.reverse.binary_map
"""

from __future__ import annotations

from capture_recovery.reverse.binary_map import (
    BinaryMap,
    BinaryNode,
)


def test_empty_buffer_returns_empty_list():
    assert BinaryMap.scan(b"") == []


def test_returns_binarynode_instances():
    nodes = BinaryMap.scan(b"Hello")

    assert len(nodes) == 1
    assert isinstance(nodes[0], BinaryNode)


def test_detect_ascii_string():
    nodes = BinaryMap.scan(b"Hello World")

    assert len(nodes) == 1

    node = nodes[0]

    assert node.kind == "ascii"
    assert node.offset == 0
    assert node.length == 11
    assert node.value == "Hello World"


def test_detect_ascii_after_binary_prefix():
    data = b"\x00\x01\x02Hello"

    nodes = BinaryMap.scan(data)

    assert len(nodes) == 1
    assert nodes[0].offset == 3
    assert nodes[0].value == "Hello"


def test_ignore_short_ascii_strings():
    assert BinaryMap.scan(b"ABC") == []


def test_detect_multiple_ascii_strings():
    data = b"Hello\x00World"

    nodes = BinaryMap.scan(data)

    assert len(nodes) == 2

    assert nodes[0].value == "Hello"
    assert nodes[1].value == "World"


def test_detect_zero_block():
    data = b"\x00" * 8

    nodes = BinaryMap.scan(data)

    assert len(nodes) == 1

    node = nodes[0]

    assert node.kind == "zero_block"
    assert node.offset == 0
    assert node.length == 8
    assert node.value is None


def test_ignore_short_zero_block():
    assert BinaryMap.scan(b"\x00" * 7) == []


def test_detect_multiple_zero_blocks():
    data = (
        b"\x00" * 8
        + b"Hello"
        + b"\x00" * 10
    )

    nodes = BinaryMap.scan(data)

    zero_nodes = [
        n for n in nodes
        if n.kind == "zero_block"
    ]

    assert len(zero_nodes) == 2

    assert zero_nodes[0].length == 8
    assert zero_nodes[1].length == 10


def test_nodes_are_sorted_by_offset():
    data = (
        b"\x00" * 8
        + b"Hello"
    )

    nodes = BinaryMap.scan(data)

    offsets = [n.offset for n in nodes]

    assert offsets == sorted(offsets)


def test_memoryview_supported():
    data = memoryview(b"Hello")

    nodes = BinaryMap.scan(data)

    assert len(nodes) == 1
    assert nodes[0].value == "Hello"


def test_bytearray_supported():
    data = bytearray(b"Hello")

    nodes = BinaryMap.scan(data)

    assert len(nodes) == 1
    assert nodes[0].value == "Hello"


def test_ascii_node_fields():
    node = BinaryMap.scan(b"Fixture")[0]

    assert node.offset == 0
    assert node.length == 7
    assert node.kind == "ascii"
    assert node.value == "Fixture"


def test_zero_block_fields():
    node = BinaryMap.scan(b"\x00" * 12)[0]

    assert node.offset == 0
    assert node.length == 12
    assert node.kind == "zero_block"
    assert node.value is None


def test_binary_data_without_patterns():
    data = bytes([1, 2, 3, 128, 255, 10])

    assert BinaryMap.scan(data) == []


def test_ascii_between_zero_blocks():
    data = (
        b"\x00" * 8
        + b"Capture"
        + b"\x00" * 8
    )

    nodes = BinaryMap.scan(data)

    assert len(nodes) == 3

    assert nodes[0].kind == "zero_block"
    assert nodes[1].kind == "ascii"
    assert nodes[2].kind == "zero_block"


def test_ascii_length_is_exact():
    node = BinaryMap.scan(b"Capture2024")[0]

    assert node.length == len("Capture2024")


def test_zero_block_offset():
    data = b"Hello" + b"\x00" * 8

    node = [
        n
        for n in BinaryMap.scan(data)
        if n.kind == "zero_block"
    ][0]

    assert node.offset == 5


def test_scan_returns_new_list():
    a = BinaryMap.scan(b"Hello")
    b = BinaryMap.scan(b"Hello")

    assert a is not b


def test_binarynode_is_hashable():
    node = BinaryMap.scan(b"Hello")[0]

    assert hash(node)