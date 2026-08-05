from __future__ import annotations

import json

from dataclasses import asdict
from pathlib import Path


from capture_recovery.research.reference_corpus_builder import (
    ReferenceCorpus,
)

from capture_recovery.research.reference_object_extractor import (
    ReferenceObject,
)

from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
)



class CorpusStore:
    """
    Persistent storage for reference corpus.

    Format:
    JSON

    Stores:
    - projects
    - extracted objects
    - signatures
    - binary data
    """



    VERSION = 1



    def save(
        self,
        corpus: ReferenceCorpus,
        destination: Path,
    ) -> None:
        """
        Save corpus to JSON file.
        """

        data = {
            "version": self.VERSION,

            "projects": [
                str(project)
                for project
                in corpus.projects
            ],

            "objects": [
                {
                    "object_type": obj.object_type,

                    "offset": obj.offset,

                    "size": obj.size,

                    "signature": obj.signature,

                    "data": (
                        obj.data.hex()
                    ),

                    "confidence": obj.confidence,
                }

                for obj
                in corpus.objects
            ],
        }


        destination.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )



    def load(
        self,
        source: Path,
    ) -> ReferenceCorpus:
        """
        Load corpus from JSON.
        """

        data = json.loads(
            source.read_text(
                encoding="utf-8"
            )
        )


        objects = tuple(
            ReferenceObject(
                object_type=item["object_type"],

                offset=item["offset"],

                size=item["size"],

                signature=item["signature"],

                data=bytes.fromhex(
                    item["data"]
                ),

                confidence=item["confidence"],
            )

            for item
            in data.get(
                "objects",
                [],
            )
        )


        return ReferenceCorpus(
            projects=tuple(
                Path(project)
                for project
                in data.get(
                    "projects",
                    [],
                )
            ),

            objects=objects,

            library=ObjectLibrary(),
        )