from capture_recovery.discovery import EnumConstraint


def test_name():
    constraint = EnumConstraint((1, 2, 3))

    assert constraint.name == "EnumConstraint"


def test_matches_known_values():
    constraint = EnumConstraint((0, 1, 2))

    assert constraint.matches(0)
    assert constraint.matches(1)
    assert constraint.matches(2)


def test_rejects_unknown_value():
    constraint = EnumConstraint((0, 1, 2))

    assert not constraint.matches(3)


def test_duplicates_removed():
    constraint = EnumConstraint((1, 2, 2, 3, 1))

    assert constraint.values == (1, 2, 3)


def test_empty_enum():
    constraint = EnumConstraint(())

    assert constraint.values == ()
    assert not constraint.matches(0)