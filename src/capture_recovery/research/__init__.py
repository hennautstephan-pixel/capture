"""
Research package.

Reverse engineering, corpus analysis,
knowledge extraction and recovery strategies.
"""

from .corpus_analyzer import CorpusAnalyzer

from .corpus_diff import (
    CorpusDiff,
    CorpusDifference,
    DifferenceRegion,
)

from .models import (
    CorpusAnalysis,
    CorpusStream,
)

from .corpus_statistics import (
    CorpusStatistics,
    CorpusStatisticsAnalyzer,
)

from .corpus_report import (
    CorpusReport,
    CorpusReportGenerator,
)

from .corpus_matrix import (
    CorpusMatrix,
    CorpusMatrixAnalyzer,
    MatrixEntry,
)

from .corpus_patterns import (
    CorpusPatterns,
    CorpusPatternsAnalyzer,
    PatternRegion,
)

from .pattern_merger import (
    MergedPatternRegion,
    MergedPatterns,
    PatternMerger,
)

from .structure_mapper import (
    CandidateStructure,
    StructureMap,
    StructureMapper,
)

from .field_mapper import (
    FieldCandidate,
    FieldMap,
    FieldMapper,
)

from .knowledge_base import (
    KnowledgeBase,
    KnowledgeBaseBuilder,
    KnowledgeEntry,
)

from .field_correlator import (
    CorrelationReport,
    FieldCorrelation,
    FieldCorrelator,
)

from .object_mapper import (
    CandidateObject,
    ObjectMap,
    ObjectMapper,
)

from .project_layout import (
    LayoutRegion,
    ProjectLayout,
    ProjectLayoutBuilder,
    RegionKind,
)

from .integrity_analyzer import (
    IntegrityAnalyzer,
    IntegrityIssue,
    IntegrityReport,
    IntegritySeverity,
)

from .repair_strategy import (
    RepairAction,
    RepairPlan,
    RepairPriority,
    RepairStep,
    RepairStrategy,
)

from .repair_plan import (
    ExecutionPlan,
    RepairOperation,
    RepairPhase,
    RepairPlanner,
    RepairTask,
)

from .stream_rebuilder import (
    RebuiltChunk,
    StreamRebuilder,
    StreamRebuildResult,
)

from .project_rebuilder import (
    ProjectImage,
    ProjectRebuilder,
    ProjectRebuildResult,
)

from .repair_engine import (
    RepairEngine,
    RepairEngineResult,
)

from .recovery_pipeline import (
    RecoveryPipeline,
    RecoveryResult,
)

from .corpus_knowledge import (
    CorpusKnowledgeBase,
    CorpusKnowledgeEntry,
    CorpusSample,
)

from .corpus_builder import (
    CorpusBuilder,
    CorpusBuildResult,
)

from .corpus_exporter import (
    CorpusExporter,
)

from .corpus_loader import (
    CorpusLoader,
)

from .corpus_classifier import (
    CorpusClassifier,
    ClassificationResult,
)

from .reference_project_analyzer import (
    ReferenceProjectAnalyzer,
    ReferenceProjectModel,
    ReferenceBlock,
)

from .reference_object_extractor import (
    ReferenceObjectExtractor,
    ReferenceObject,
)

from .reference_library_builder import (
    ReferenceLibraryBuilder,
    ReferenceLibraryResult,
)

from .reference_corpus_builder import (
    ReferenceCorpusBuilder,
    ReferenceCorpus,
    ReferenceCorpusBuildResult,
)

from .corpus_pipeline import (
    CorpusPipeline,
    CorpusPipelineResult,
)

from .corpus_store import (
    CorpusStore,
)

from .object_signature_index import (
    ObjectSignatureIndex,
    SignatureLookupResult,
)


__all__ = [
    "CorpusAnalyzer",

    "CorpusDiff",
    "CorpusDifference",
    "DifferenceRegion",

    "CorpusAnalysis",
    "CorpusStream",

    "CorpusStatistics",
    "CorpusStatisticsAnalyzer",

    "CorpusReport",
    "CorpusReportGenerator",

    "CorpusMatrix",
    "CorpusMatrixAnalyzer",
    "MatrixEntry",

    "CorpusPatterns",
    "CorpusPatternsAnalyzer",
    "PatternRegion",

    "MergedPatternRegion",
    "MergedPatterns",
    "PatternMerger",

    "CandidateStructure",
    "StructureMap",
    "StructureMapper",

    "FieldCandidate",
    "FieldMap",
    "FieldMapper",

    "KnowledgeBase",
    "KnowledgeBaseBuilder",
    "KnowledgeEntry",

    "CorrelationReport",
    "FieldCorrelation",
    "FieldCorrelator",

    "CandidateObject",
    "ObjectMap",
    "ObjectMapper",

    "LayoutRegion",
    "ProjectLayout",
    "ProjectLayoutBuilder",
    "RegionKind",

    "IntegrityAnalyzer",
    "IntegrityIssue",
    "IntegrityReport",
    "IntegritySeverity",

    "RepairAction",
    "RepairPlan",
    "RepairPriority",
    "RepairStep",
    "RepairStrategy",

    "ExecutionPlan",
    "RepairOperation",
    "RepairPhase",
    "RepairPlanner",
    "RepairTask",

    "RebuiltChunk",
    "StreamRebuilder",
    "StreamRebuildResult",

    "ProjectImage",
    "ProjectRebuilder",
    "ProjectRebuildResult",

    "RepairEngine",
    "RepairEngineResult",

    "RecoveryPipeline",
    "RecoveryResult",

    "CorpusKnowledgeBase",
    "CorpusKnowledgeEntry",
    "CorpusSample",

    "CorpusBuilder",
    "CorpusBuildResult",

    "CorpusExporter",

    "CorpusLoader",

    "CorpusClassifier",
    "ClassificationResult",

    "ReferenceProjectAnalyzer",
    "ReferenceProjectModel",
    "ReferenceBlock",

    "ReferenceObjectExtractor",
    "ReferenceObject",

    "ReferenceLibraryBuilder",
    "ReferenceLibraryResult",

    "ReferenceCorpusBuilder",
    "ReferenceCorpus",
    "ReferenceCorpusBuildResult",

    "CorpusPipeline",
    "CorpusPipelineResult",

    "CorpusStore",

    "ObjectSignatureIndex",
    "SignatureLookupResult",
]