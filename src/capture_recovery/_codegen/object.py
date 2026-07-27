Fixture = (
    Object("Fixture")
        .string("name", required=True)
        .uint16("universe", required=True)
        .uint16("address", required=True)
        .vector3("position")
        .vector3("rotation")
)