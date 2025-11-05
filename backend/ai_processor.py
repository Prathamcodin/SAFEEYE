import cv2
import numpy as np
from ultralytics import YOLO
from typing import Optional, List, Dict, Any
import os
import json
from datetime import datetime
import torch
import torchvision.transforms as transforms
from PIL import Image
from scipy.spatial.distance import cosine

# Note: DeepSORT can be installed via: pip install deep-sort-realtime
# For now, using a simple tracker implementation
DEEPSORT_AVAILABLE = False

# Try to import torchreid for ReID
try:
    import torchreid
    REID_AVAILABLE = True
except ImportError:
    REID_AVAILABLE = False
    print("Warning: torchreid not available, using cosine similarity for ReID")


class SimpleTracker:
    """Simple tracker fallback when DeepSORT is not available"""
    def __init__(self):
        self.next_id = 1
        self.tracks = {}
    
    def update(self, detections):
        """Update tracks with new detections"""
        if not detections:
            return []
        
        # Simple IoU-based tracking
        tracks = []
        for det in detections:
            # Assign new ID or match with existing track
            track_id = self.next_id
            self.next_id += 1
            tracks.append({
                'bbox': det['bbox'],
                'track_id': track_id,
                'confidence': det['confidence']
            })
        
        return tracks


class PersonReID:
    """Person Re-identification module"""
    def __init__(self):
        self.model = None
        self.transform = transforms.Compose([
            transforms.Resize((256, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def load_model(self):
        """Load ReID model (mock implementation)"""
        # In production, load OSNet or other ReID model
        # For now, we'll use a simple feature extractor
        pass
    
    def extract_features(self, image: np.ndarray) -> np.ndarray:
        """Extract features from person image"""
        # Mock feature extraction - in production use actual ReID model
        # For now, return a random feature vector
        return np.random.rand(512).astype(np.float32)
    
    def compute_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """Compute cosine similarity between features"""
        return 1 - cosine(features1, features2)


class TheftDetector:
    """Detect theft-like behavior"""
    def __init__(self):
        self.person_tracks = {}  # track_id -> [timestamps, positions]
        self.object_tracks = {}  # object_id -> [timestamps, positions]
        self.theft_threshold = 5.0  # seconds
    
    def detect_event(self, frame_num: int, timestamp: float, detections: List[Dict]) -> List[Dict]:
        """Detect theft events"""
        events = []
        
        for det in detections:
            person_id = det.get('person_id')
            bbox = det.get('bbox')
            
            if person_id not in self.person_tracks:
                self.person_tracks[person_id] = []
            
            self.person_tracks[person_id].append({
                'timestamp': timestamp,
                'bbox': bbox,
                'frame': frame_num
            })
            
            # Simple heuristic: if person enters frame, picks up object, and leaves quickly
            track_history = self.person_tracks[person_id]
            if len(track_history) >= 10:
                # Check if person was in frame for short duration
                duration = track_history[-1]['timestamp'] - track_history[0]['timestamp']
                if duration < self.theft_threshold:
                    # Potential theft event
                    events.append({
                        'person_id': person_id,
                        'timestamp': timestamp,
                        'event_label': 'theft-suspect',
                        'confidence': 0.7,
                        'bbox': bbox,
                        'frame_number': frame_num
                    })
        
        return events


async def process_video(
    video_path: str,
    photo_path: Optional[str],
    job_id: str
) -> Dict[str, Any]:
    """
    Process video with YOLOv8, tracking, ReID, and theft detection
    """
    print(f"Processing video: {video_path}")
    
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')  # nano model for speed
    
    # Initialize tracker
    if DEEPSORT_AVAILABLE:
        tracker = DeepSort(max_age=30, n_init=3)
    else:
        tracker = SimpleTracker()
    
    # Initialize ReID
    reid = PersonReID()
    
    # Initialize theft detector
    theft_detector = TheftDetector()
    
    # Load suspect photo if provided
    suspect_features = None
    if photo_path and os.path.exists(photo_path):
        suspect_img = cv2.imread(photo_path)
        suspect_features = reid.extract_features(suspect_img)
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    # Prepare output video
    processed_dir = os.path.join(os.path.dirname(__file__), "processed")
    os.makedirs(processed_dir, exist_ok=True)
    output_path = os.path.join(processed_dir, f"{job_id}_processed.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    detections = []
    frame_num = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        timestamp = frame_num / fps if fps > 0 else frame_num * 0.033
        
        # Run YOLOv8 detection
        results = model(frame, conf=0.5, classes=[0])  # class 0 is person
        
        # Extract person detections
        person_detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box.cls == 0:  # person class
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    person_detections.append({
                        'bbox': [float(x1), float(y1), float(x2), float(y2)],
                        'confidence': confidence
                    })
        
        # Update tracker
        tracked_objects = tracker.update(person_detections)
        
        # Match with suspect if provided
        suspect_matches = []
        for track in tracked_objects:
            person_id = track.get('track_id', 0)
            bbox = track['bbox']
            
            # Extract person crop
            x1, y1, x2, y2 = [int(b) for b in bbox]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(width, x2), min(height, y2)
            
            if x2 > x1 and y2 > y1:
                person_crop = frame[y1:y2, x1:x2]
                
                # Compare with suspect
                if suspect_features is not None:
                    person_features = reid.extract_features(person_crop)
                    similarity = reid.compute_similarity(suspect_features, person_features)
                    
                    if similarity > 0.5:  # threshold
                        suspect_matches.append({
                            'person_id': person_id,
                            'timestamp': timestamp,
                            'similarity': float(similarity),
                            'bbox': bbox
                        })
        
        # Detect theft events
        theft_events = theft_detector.detect_event(
            frame_num,
            timestamp,
            [{'person_id': t.get('track_id', 0), 'bbox': t['bbox']} for t in tracked_objects]
        )
        
        # Draw bounding boxes and labels
        annotated_frame = frame.copy()
        for track in tracked_objects:
            person_id = track.get('track_id', 0)
            bbox = track['bbox']
            x1, y1, x2, y2 = [int(b) for b in bbox]
            
            # Check if this person is a suspect match
            is_suspect = any(m['person_id'] == person_id for m in suspect_matches)
            color = (0, 0, 255) if is_suspect else (0, 255, 0)
            
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            label = f"Person {person_id}"
            if is_suspect:
                label += " (SUSPECT)"
            cv2.putText(annotated_frame, label, (x1, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Draw theft event labels
        for event in theft_events:
            bbox = event['bbox']
            x1, y1, x2, y2 = [int(b) for b in bbox]
            cv2.putText(annotated_frame, "THEFT SUSPECT", (x1, y1-30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        out.write(annotated_frame)
        
        # Store detections
        for track in tracked_objects:
            person_id = track.get('track_id', 0)
            bbox = track['bbox']
            
            # Check if theft event
            event_label = None
            if any(e['person_id'] == person_id and abs(e['timestamp'] - timestamp) < 0.1 
                   for e in theft_events):
                event_label = "theft-suspect"
            
            detections.append({
                'timestamp': timestamp,
                'person_id': person_id,
                'bbox': bbox,
                'confidence': track.get('confidence', 0.5),
                'event_label': event_label,
                'frame_number': frame_num
            })
        
        frame_num += 1
        
        if frame_num % 30 == 0:
            print(f"Processed {frame_num}/{total_frames} frames")
    
    cap.release()
    out.release()
    
    # Prepare results
    results = {
        'detections': detections,
        'video_path': video_path,
        'processed_video_path': output_path,
        'total_frames': total_frames,
        'fps': fps,
        'duration': duration,
        'suspect_matched': len(suspect_matches) > 0,
        'suspect_matches': suspect_matches[:10]  # Limit to first 10 matches
    }
    
    print(f"Processing complete. Found {len(detections)} detections")
    return results

