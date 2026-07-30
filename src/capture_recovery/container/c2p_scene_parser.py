from dataclasses import dataclass
from uuid import UUID


@dataclass
class CaptureObject:
    name: str
    guid: str
    object_type: str
    color: tuple


class C2PSceneParser:

    def parse(self, data: bytes):

        objects = []

        keywords_fixture = [
            "Ape",
            "Nanlux",
            "LED",
            "PC",
            "Projecteur",
            "Spot",
        ]

        pos = 0

        while pos < len(data)-32:

            # recherche d'un nom ASCII
            if (
                32 <= data[pos] <= 126
            ):

                end = pos

                while (
                    end < len(data)
                    and 32 <= data[end] <= 126
                ):
                    end += 1

                name = data[pos:end].decode(
                    "ascii",
                    errors="ignore"
                )

                # noms intéressants seulement
                if len(name) >= 4:

                    cursor = end

                    # après le nom :
                    # couleur + paramètres + flags
                    guid_pos = cursor + 24

                    if guid_pos + 16 <= len(data):

                        raw_guid = data[
                            guid_pos:guid_pos+16
                        ]

                        try:
                            guid = str(
                                UUID(bytes=raw_guid)
                            )

                            obj_type = (
                                "fixture"
                                if any(
                                    k.lower()
                                    in name.lower()
                                    for k in keywords_fixture
                                )
                                else
                                "model"
                            )

                            objects.append(
                                CaptureObject(
                                    name=name,
                                    guid=guid,
                                    object_type=obj_type,
                                    color=tuple(
                                        data[
                                            cursor:
                                            cursor+4
                                        ]
                                    )
                                )
                            )

                        except:
                            pass

                pos=end

            else:
                pos += 1

        return objects