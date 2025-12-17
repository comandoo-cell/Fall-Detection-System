"""
Multi-Person Pose Detector using YOLOv8
======================================="""

from ultralytics import YOLO
import numpy as np
from typing import List, Dict, Tuple, Optional


class MultiPersonDetector:
    """Multi-person pose detector using YOLOv8-Pose"""
    
   
    KEYPOINT_NAMES = [
        'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
        'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
        'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
    ]
    
    def __init__(self, model_name: str = 'yolov8n-pose.pt', confidence: float = 0.5):
        """Initialize detector"""
        print(f"Model yukleniyor {model_name}...")
        self.model = YOLO(model_name)
        self.confidence = confidence
        
    def detect_people(self, frame) -> List[Dict]:
        """Detect all people in frame"""
        results = self.model(frame, conf=self.confidence, verbose=False)
        
        people = []
        
        for result in results:
            if result.keypoints is None:
                continue
                
            for person_idx in range(len(result.keypoints)):
                keypoints_data = result.keypoints[person_idx]
                
                if hasattr(keypoints_data, 'xy'):
                    kpts = keypoints_data.xy.cpu().numpy()[0]
                else:
                    continue
                
                keypoints = {}
                for i, name in enumerate(self.KEYPOINT_NAMES):
                    if i < len(kpts):
                        x, y = kpts[i]
                        if x > 0 and y > 0:
                            keypoints[name] = (int(x), int(y))
                
                bbox = None
                if result.boxes is not None and person_idx < len(result.boxes):
                    box = result.boxes[person_idx].xyxy.cpu().numpy()[0]
                    bbox = tuple(map(int, box))
                
                conf = 0.0
                if result.boxes is not None and person_idx < len(result.boxes):
                    conf = float(result.boxes[person_idx].conf.cpu().numpy()[0])
                
                people.append({
                    'keypoints': keypoints,
                    'confidence': conf,
                    'bbox': bbox
                })
        
        return people
    
    def draw_people(self, frame, people: List[Dict], draw_bbox: bool = True):
        """Draw all people on frame"""
        import cv2
        
        colors = [
            (0, 255, 0),
            (255, 0, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
        ]
        
        for idx, person in enumerate(people):
            color = colors[idx % len(colors)]
            keypoints = person['keypoints']
            
            if draw_bbox and person['bbox']:
                x1, y1, x2, y2 = person['bbox']
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                cv2.putText(frame, f"Person {idx+1}", (x1, y1-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            for name, (x, y) in keypoints.items():
                cv2.circle(frame, (x, y), 4, color, -1)
            
            self._draw_skeleton(frame, keypoints, color)
        
        return frame
    
    def _draw_skeleton(self, frame, keypoints: Dict, color: Tuple[int, int, int]):
        """Draw skeleton"""
        import cv2
        
        connections = [
            ('left_shoulder', 'right_shoulder'),
            ('left_shoulder', 'left_elbow'),
            ('left_elbow', 'left_wrist'),
            ('right_shoulder', 'right_elbow'),
            ('right_elbow', 'right_wrist'),
            ('left_shoulder', 'left_hip'),
            ('right_shoulder', 'right_hip'),
            ('left_hip', 'right_hip'),
            ('left_hip', 'left_knee'),
            ('left_knee', 'left_ankle'),
            ('right_hip', 'right_knee'),
            ('right_knee', 'right_ankle'),
        ]
        
        for point1, point2 in connections:
            if point1 in keypoints and point2 in keypoints:
                cv2.line(frame, keypoints[point1], keypoints[point2], color, 2)

