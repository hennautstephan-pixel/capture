from capture_recovery.models.project import Project


class Dummy:
    def __init__(self, t, i):
        self.object_type = t
        self.identifier = i


def test_add():
    p = Project()

    obj = Dummy("Fixture", 1)

    p.add(obj)

    assert len(p) == 1


def test_remove():
    p = Project()

    obj = Dummy("Fixture", 1)

    p.add(obj)

    p.remove(obj)

    assert len(p) == 0


def test_clear():
    p = Project()

    p.add(Dummy("Fixture", 1))
    p.add(Dummy("Universe", 2))

    p.clear()

    assert len(p) == 0


def test_statistics():
    p = Project()

    p.add(Dummy("Fixture", 1))
    p.add(Dummy("Fixture", 2))
    p.add(Dummy("Universe", 3))

    stats = p.statistics()

    assert stats["Fixture"] == 2
    assert stats["Universe"] == 1


def test_object_types():
    p = Project()

    p.add(Dummy("Fixture", 1))
    p.add(Dummy("Universe", 2))

    assert p.object_types == (
        "Fixture",
        "Universe",
    )


def test_find():
    p = Project()

    obj = Dummy("Fixture", 10)

    p.add(obj)

    assert p.find("Fixture", 10) is obj


def test_metadata():
    p = Project()

    p.metadata["version"] = "2024"

    assert p.metadata["version"] == "2024"