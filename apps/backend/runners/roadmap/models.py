"""
Data models for roadmap generation.
"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RoadmapPhaseResult:
    """Result of a roadmap phase execution."""

    phase: str
    success: bool
    output_files: list[str]
    errors: list[str]
    retries: int


@dataclass
class RoadmapConfig:
    """Configuration for roadmap generation."""

    project_dir: Path
    output_dir: Path
    model: str = os.environ.get(
        "ANTHROPIC_DEFAULT_OPUS_MODEL", "claude-opus-4-5-20251101"
    )
    refresh: bool = False  # Force regeneration even if roadmap exists
    enable_competitor_analysis: bool = False  # Enable competitor analysis phase
