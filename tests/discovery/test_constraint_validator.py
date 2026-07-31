from capture_recovery.discovery import (
    BitmaskConstraint,
    ConstraintValidator,
    EnumConstraint,
    RangeConstraint,
    StepConstraint,
)


def test_empty():

    validator = ConstraintValidator()

    result = validator.validate(())

    assert result.valid
    assert result.conflicts == ()


def test_single_constraint():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            RangeConstraint(
                minimum=0,
                maximum=255,
            ),
        )
    )

    assert result.valid


def test_overlapping_ranges():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            RangeConstraint(0, 100),
            RangeConstraint(50, 200),
        )
    )

    assert result.valid


def test_disjoint_ranges():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            RangeConstraint(0, 100),
            RangeConstraint(200, 300),
        )
    )

    assert not result.valid

    assert len(result.conflicts) == 1

    assert result.conflicts[0].reason == "disjoint ranges"


def test_enum_inside_range():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            RangeConstraint(0, 255),
            EnumConstraint((0, 64, 128, 255)),
        )
    )

    assert result.valid


def test_enum_outside_range():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            RangeConstraint(0, 255),
            EnumConstraint((0, 64, 512)),
        )
    )

    assert not result.valid

    assert result.conflicts[0].reason == "enum outside range"


def test_overlapping_enums():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            EnumConstraint((1, 2, 3)),
            EnumConstraint((3, 4, 5)),
        )
    )

    assert result.valid


def test_disjoint_enums():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            EnumConstraint((1, 2)),
            EnumConstraint((10, 20)),
        )
    )

    assert not result.valid

    assert result.conflicts[0].reason == "disjoint enums"


def test_compatible_steps():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            StepConstraint(5),
            StepConstraint(10),
        )
    )

    assert result.valid


def test_incompatible_steps():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            StepConstraint(6),
            StepConstraint(10),
        )
    )

    assert not result.valid

    assert result.conflicts[0].reason == "incompatible steps"


def test_compatible_bitmasks():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            BitmaskConstraint(0x03),
            BitmaskConstraint(0x07),
        )
    )

    assert result.valid


def test_independent_bitmasks():

    validator = ConstraintValidator()

    result = validator.validate(
        (
            BitmaskConstraint(0x01),
            BitmaskConstraint(0x80),
        )
    )

    assert not result.valid

    assert result.conflicts[0].reason == "independent bitmasks"