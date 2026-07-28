"""
Capture project reader.

Reads Capture project files (.c2p)
and extracts recoverable information.
"""

from __future__ import annotations

from pathlib import Path
import json
import zipfile
import xml.etree.ElementTree as ET

from .capture_container_analyzer import (
    CaptureContainerAnalyzer,
)


class CaptureProjectReader:
    """
    Reader for Capture project files.
    """


    SUPPORTED_EXTENSIONS = {
        ".c2p",
        ".c2",
        ".cap",
    }


    def __init__(
        self,
        analyzer: CaptureContainerAnalyzer | None = None,
    ):

        self.analyzer = (
            analyzer
            if analyzer is not None
            else CaptureContainerAnalyzer()
        )


    def read(
        self,
        path,
    ) -> dict:

        path = Path(path)


        if not path.exists():

            raise FileNotFoundError(
                path
            )


        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:

            raise ValueError(
                f"Unsupported Capture format: {path.suffix}"
            )


        project = {

            "file": str(path),

            "name": path.stem,

            "fixtures": [],

            "groups": [],

            "scenes": [],

            "patch": [],

            "metadata": {},

        }


        if zipfile.is_zipfile(path):

            self._read_archive(
                path,
                project,
            )

        else:

            self._read_binary(
                path,
                project,
            )


        self._analyze(
            project
        )


        return project



    def _analyze(
        self,
        project,
    ):
        """
        Convert extracted metadata into
        semantic project objects.
        """

        analysis = self.analyzer.analyze(
            project["metadata"]
        )


        project["fixtures"] = (
            analysis.get(
                "fixtures",
                [],
            )
        )


        project["groups"] = (
            analysis.get(
                "groups",
                [],
            )
        )


        project["scenes"] = (
            analysis.get(
                "scenes",
                [],
            )
        )


        project["patch"] = (
            analysis.get(
                "patch",
                [],
            )
        )


        project["metadata"]["analysis"] = (
            analysis
        )



    def _read_archive(
        self,
        path,
        project,
    ):

        with zipfile.ZipFile(
            path,
            "r",
        ) as archive:


            files = archive.namelist()


            project["metadata"]["files"] = files


            for filename in files:

                lower = filename.lower()


                if lower.endswith(".json"):

                    self._read_json(
                        archive,
                        filename,
                        project,
                    )


                elif lower.endswith(".xml"):

                    self._read_xml(
                        archive,
                        filename,
                        project,
                    )



    def _read_json(
        self,
        archive,
        filename,
        project,
    ):

        try:

            data = json.loads(

                archive.read(
                    filename
                ).decode(
                    "utf-8"
                )

            )


            project["metadata"][filename] = data


        except Exception:

            pass



    def _read_xml(
        self,
        archive,
        filename,
        project,
    ):

        try:

            root = ET.fromstring(

                archive.read(
                    filename
                )

            )


            project["metadata"][filename] = {
                "root": root.tag
            }


        except Exception:

            pass



    def _read_binary(
        self,
        path,
        project,
    ):

        data = path.read_bytes()


        project["metadata"]["size"] = (
            len(data)
        )


        project["metadata"]["header"] = (
            data[:64].hex()
        )


        project["metadata"]["ascii_strings"] = (
            self._extract_ascii_strings(
                data
            )
        )


        project["metadata"]["utf16_strings"] = (
            self._extract_utf16_strings(
                data
            )
        )



    def _extract_ascii_strings(
        self,
        data,
        minimum=4,
    ):

        result = []

        current = bytearray()


        for byte in data:

            if 32 <= byte <= 126:

                current.append(
                    byte
                )

            else:

                if len(current) >= minimum:

                    result.append(
                        current.decode(
                            "ascii",
                            errors="ignore",
                        )
                    )

                current.clear()


        return result[:200]



    def _extract_utf16_strings(
        self,
        data,
        minimum=4,
    ):

        result = []


        try:

            text = data.decode(
                "utf-16-le",
                errors="ignore",
            )


            for part in text.split("\x00"):

                if len(part) >= minimum:

                    result.append(
                        part
                    )


        except Exception:

            pass


        return result[:200]