from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Detection(BaseModel):
    timestamp: float  # seconds
    person_id: int
    bbox: List[float]  # [x1, y1, x2, y2]
    confidence: float
    event_label: Optional[str] = None  # e.g., "theft-suspect"
    frame_number: int


class JobResults(BaseModel):
    detections: List[Detection]
    video_path: str
    processed_video_path: Optional[str] = None
    total_frames: int
    fps: float
    duration: float
    suspect_matched: bool = False
    suspect_matches: Optional[List[Dict[str, Any]]] = None

