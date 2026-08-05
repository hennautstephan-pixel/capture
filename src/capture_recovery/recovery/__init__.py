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

from .intelligent_repair_adapter import (
    IntelligentRepairAdapter,
    AdaptedRepairPlan,
)

from .intelligent_restore_action import (
    IntelligentRestoreAction,
)

from .intelligent_repair_executor import (
    IntelligentRepairExecutor,
    IntelligentExecutionResult,
)

from .intelligent_recovery_pipeline import (
    IntelligentRecoveryPipeline,
    IntelligentRecoveryResult,
)

from .binary_repair_writer import (
    BinaryRepairWriter,
    BinaryRepairOperation,
    BinaryRepairResult,
)

from .binary_repair_executor import (
    BinaryRepairExecutor,
    BinaryExecutionResult,
)

from .full_recovery_engine import (
    FullRecoveryEngine,
    RecoveryReport,
)

from .full_recovery_pipeline import (
    FullRecoveryPipeline,
    FullRecoveryResult,
)

from .recovery_report_generator import (
    RecoveryReportGenerator,
    RecoveryReport,
)

from .file_recovery_engine import (
    FileRecoveryEngine,
    FileRecoveryResult,
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
    "IntelligentRepairAdapter",
    "AdaptedRepairPlan",
    "IntelligentRestoreAction",
    "IntelligentRepairExecutor",
    "IntelligentExecutionResult",
    "IntelligentRecoveryPipeline",
    "IntelligentRecoveryResult",
    "BinaryRepairWriter",
    "BinaryRepairOperation",
    "BinaryRepairResult",
    "BinaryRepairExecutor",
    "BinaryExecutionResult",
    "FullRecoveryEngine",
    "RecoveryReport",
    "FullRecoveryPipeline",
    "FullRecoveryResult",
    "RecoveryReportGenerator",
    "RecoveryReport",
    "FileRecoveryEngine",
    "FileRecoveryResult"
]