"""
capture_recovery.reverse.string_detector

Detect strings inside binary buffers.
"""

from __future__ import annotations


from collections.abc import Iterable


from .detection_options import DetectionOptions

from .detector_type import DetectorType

from .string_type import (
    STRING_TYPES,
    StringType,
)

from .string_value import (
    StringValue,
)



class StringDetector:
    """
    Detect readable strings.
    """



    def __init__(
        self,
        string_types: Iterable[StringType] = STRING_TYPES,
        minimum_length: int = 4,
    ) -> None:


        self._string_types = tuple(
            string_types
        )


        self.minimum_length = minimum_length



    @property
    def name(
        self,
    ) -> str:

        return "string"



    @property
    def string_types(
        self,
    ) -> tuple[StringType, ...]:

        return self._string_types



    def detect(
        self,
        data,
        options: DetectionOptions | None = None,
        min_length: int | None = None,
    ) -> list[StringValue]:


        if options is None:

            options = DetectionOptions()



        if min_length is None:

            min_length = self.minimum_length



        if hasattr(
            options,
            "enabled_types",
        ):

            enabled = options.enabled_types


            if enabled is not None:

                if DetectorType.STRING not in enabled:

                    return []



        buffer = bytes(
            data
        )



        if options.max_scan_size is not None:

            buffer = buffer[
                :options.max_scan_size
            ]



        results = []



        for string_type in self._string_types:


            if string_type.name == "ascii":


                results.extend(

                    self._scan_ascii(

                        buffer,

                        string_type,

                        min_length,

                    )

                )



            elif string_type.name in (

                "utf16",

                "utf16-le",

                "utf16_le",

            ):


                results.extend(

                    self._scan_utf16(

                        buffer,

                        string_type,

                        min_length,

                    )

                )



            elif string_type.name == "utf16_be":


                results.extend(

                    self._scan_utf16_be(

                        buffer,

                        string_type,

                        min_length,

                    )

                )



        return self._remove_duplicates(
            results
        )





    def _scan_ascii(
        self,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
    ) -> list[StringValue]:


        results = []

        start = None



        for index, byte in enumerate(data):


            if 32 <= byte <= 126:


                if start is None:

                    start = index



            else:


                if start is not None:


                    raw = data[
                        start:index
                    ]


                    value = raw.decode(

                        string_type.encoding,

                        errors="ignore",

                    )



                    if self._valid(

                        value,

                        minimum_length,

                    ):


                        results.append(

                            StringValue(

                                offset=start,

                                string_type=string_type,

                                value=value,

                                raw_bytes=raw,

                                terminated=True,

                            )

                        )


                    start = None



        return results





    def _scan_utf16(
        self,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
    ) -> list[StringValue]:


        results = []

        start = None

        index = 0



        while index + 1 < len(data):


            pair = data[
                index:index + 2
            ]



            valid_utf16_char = (

                pair[1] == 0

                and

                32 <= pair[0] <= 126

            )



            if valid_utf16_char:


                if start is None:

                    start = index



            else:


                if start is not None:


                    raw = data[
                        start:index
                    ]



                    try:

                        value = raw.decode(

                            string_type.encoding,

                            errors="ignore",

                        )


                    except Exception:

                        value = ""



                    if self._valid(

                        value,

                        minimum_length,

                    ):


                        results.append(

                            StringValue(

                                offset=start,

                                string_type=string_type,

                                value=value,

                                raw_bytes=raw,

                                terminated=True,

                            )

                        )



                    start = None



            index += 2



        return results





    def _scan_utf16_be(
        self,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
    ) -> list[StringValue]:


        results = []

        start = None

        index = 0



        while index + 1 < len(data):


            pair = data[
                index:index + 2
            ]



            valid = (

                pair[0] == 0

                and

                32 <= pair[1] <= 126

            )



            if valid:


                if start is None:

                    start = index



            else:


                if start is not None:


                    raw = data[
                        start:index
                    ]



                    try:

                        value = raw.decode(

                            string_type.encoding,

                            errors="ignore",

                        )


                    except Exception:

                        value = ""



                    if self._valid(

                        value,

                        minimum_length,

                    ):


                        results.append(

                            StringValue(

                                offset=start,

                                string_type=string_type,

                                value=value,

                                raw_bytes=raw,

                                terminated=True,

                            )

                        )



                    start = None



            index += 2



        return results





    def _valid(
        self,
        value: str,
        minimum_length: int,
    ) -> bool:


        value = value.strip()



        if len(value) < minimum_length:

            return False



        printable = sum(

            1

            for char in value

            if char.isprintable()

        )



        if printable / len(value) < 0.8:

            return False



        letters = sum(

            1

            for char in value

            if char.isalpha()

        )



        if letters == 0:

            return False



        return True





    def _remove_duplicates(
        self,
        values: list[StringValue],
    ) -> list[StringValue]:


        result = []

        seen = set()



        for item in values:


            key = (

                item.offset,

                item.value,

            )



            if key in seen:

                continue



            seen.add(
                key
            )


            result.append(
                item
            )



        return result