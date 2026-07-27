"""
Binary differ.

Compares two binary buffers and produces BinaryChange objects.
"""

from __future__ import annotations

from itertools import zip_longest
import difflib

from .models import BinaryChange
from .models import ChangeType


class BinaryDiffer:
    """
    Performs a byte-level comparison between two binary buffers.

    The first implementation intentionally stays simple.
    Every differing byte produces one BinaryChange.

    Future versions may replace the internal algorithm
    (Myers, xdelta, bsdiff...) without changing the API.
    """

    def compare(
        self,
        before: bytes,
        after: bytes,
    ) -> tuple[BinaryChange, ...]:
        """
        Compare two binary buffers.

        Uses difflib.SequenceMatcher to detect insertions,
        deletions and replacements anywhere in the file.
        """

        changes: list[BinaryChange] = []

        matcher = difflib.SequenceMatcher(
            None,
            before,
            after,
            autojunk=False,
        )

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag == "equal":
                continue

            # ----------------------------------------------------------
            # INSERT
            # ----------------------------------------------------------

            if tag == "insert":

                for offset_after in range(j1, j2):

                    changes.append(
                        BinaryChange(
                            offset=i1,
                            before=b"",
                            after=bytes((after[offset_after],)),
                            change_type=ChangeType.INSERT,
                        )
                    )

                continue

            # ----------------------------------------------------------
            # DELETE
            # ----------------------------------------------------------

            if tag == "delete":

                for offset_before in range(i1, i2):

                    changes.append(
                        BinaryChange(
                            offset=offset_before,
                            before=bytes((before[offset_before],)),
                            after=b"",
                            change_type=ChangeType.DELETE,
                        )
                    )

                continue

            # ----------------------------------------------------------
            # REPLACE
            # ----------------------------------------------------------

            if tag == "replace":

                common = min(i2 - i1, j2 - j1)

                # Modified bytes

                for n in range(common):

                    changes.append(
                        BinaryChange(
                            offset=i1 + n,
                            before=bytes((before[i1 + n],)),
                            after=bytes((after[j1 + n],)),
                            change_type=ChangeType.MODIFY,
                        )
                    )

                # Extra deleted bytes

                for n in range(common, i2 - i1):

                    changes.append(
                        BinaryChange(
                            offset=i1 + n,
                            before=bytes((before[i1 + n],)),
                            after=b"",
                            change_type=ChangeType.DELETE,
                        )
                    )

                # Extra inserted bytes

                for n in range(common, j2 - j1):

                    changes.append(
                        BinaryChange(
                            offset=i2,
                            before=b"",
                            after=bytes((after[j1 + n],)),
                            change_type=ChangeType.INSERT,
                        )
                    )

        return tuple(changes)
    # ==================================================================
    # Convenience methods
    # ==================================================================

    def compare_files(
        self,
        before_path: str,
        after_path: str,
    ) -> tuple[BinaryChange, ...]:
        """
        Compare two binary files.

        Parameters
        ----------
        before_path:
            Path of the original file.

        after_path:
            Path of the modified file.
        """

        with open(before_path, "rb") as fp:
            before = fp.read()

        with open(after_path, "rb") as fp:
            after = fp.read()

        return self.compare(before, after)

