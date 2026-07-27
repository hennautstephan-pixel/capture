from capture_recovery._codegen.object import Object


def test_fixture_definition():
    fixture = (
        Object("Fixture")
        .string("name", required=True)
        .uint16("universe", required=True)
        .vector3("position")
    )

    assert fixture.name == "Fixture"
    assert len(fixture.fields) == 3
    assert fixture.fields[0].name == "name"
    assert fixture.fields[0].required is True