"""
Recovery framework.

Provides integrity checking and project/object repair utilities.
"""

from .integrity_issue import (
    IntegrityIssue,
    IntegritySeverity,
)

from .integrity_report import (
    IntegrityReport,
)

from .project_integrity_checker import (
    ProjectIntegrityChecker,
)

from .project_repair_engine import (
    ProjectRepairEngine,
)

from .object_repair_engine import (
    ObjectRepairEngine,
)

from .repair_action import (
    RepairAction,
    RepairResult,
    RepairStatus,
)

from .repair_missing_collections_action import (
    RepairMissingCollectionsAction,
)

from .intelligent_repair_engine import (
    IntelligentRepairEngine,
    IntelligentRepairCandidate,
    IntelligentRepairResult,
)

__all__ = [
    "IntegrityIssue",
    "IntegritySeverity",
    "IntegrityReport",
    "ProjectIntegrityChecker",
    "ProjectRepairEngine",
    "ObjectRepairEngine",
    "RepairAction",
    "RepairResult",
    "RepairStatus",
    "RepairMissingCollectionsAction",
    "IntelligentRepairEngine",
    "IntelligentRepairCandidate",
    "IntelligentRepairResult",
]