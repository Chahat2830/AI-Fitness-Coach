import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict


@dataclass
class AnalysisMetadata:
    """Tracks systemic diagnostics and engine execution identifiers."""
    
    scan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scan_time: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    analysis_version: str = "1.2"
    vision_model: str = "MediaPipe Pose"
    ai_model: str = "Gemini 2.5 Flash"
    processing_time_sec: float = 0.0


@dataclass
class AnalysisReport:
    """Master analytical wrapper containing all system evaluation profiles."""

    user: Dict[str, Any] = field(default_factory=dict)
    measurements: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    score: Dict[str, Any] = field(default_factory=dict)
    ai_analysis: Dict[str, Any] = field(default_factory=dict)
    workout: Dict[str, Any] = field(default_factory=dict)
    diet: Dict[str, Any] = field(default_factory=dict)
    images: Dict[str, Any] = field(default_factory=dict)
    metadata: AnalysisMetadata = field(default_factory=AnalysisMetadata)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the dataclass tree into a clean native dictionary.
        
        Ensures perfect downstream compatibility with json.dump and Streamlit views.
        """
        return asdict(self)