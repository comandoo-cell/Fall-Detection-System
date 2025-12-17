"""
Fall Detection Logic Module
==========================="""

import numpy as np
from typing import Dict, Tuple, Optional, List
from collections import deque


class FallDetector:
    """Fall Detector - Enhanced fall detection using multi-criteria analysis"""
    
    def __init__(self, 
                 angle_threshold: float = 60.0,
                 history_size: int = 10):
        """Initialize fall detector"""
        self.angle_threshold = angle_threshold
        self.history_size = history_size
        
        self.angle_history = deque(maxlen=5)
        self.aspect_ratio_history = deque(maxlen=5)
        
        self.is_fallen = False
        self.fall_start_time = None
        self.fall_frames_count = 0
        self.confidence_score = 0.0
        
        self.initial_check_frames = 0
        self.max_initial_angle = 0
        
    def calculate_angle(self, point1: Tuple[int, int], 
                       point2: Tuple[int, int]) -> float:
        """Calculate angle between two points"""
        x1, y1 = point1
        x2, y2 = point2
        
        angle_rad = np.arctan2(abs(y2 - y1), abs(x2 - x1))
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
    
    def calculate_body_angle(self, keypoints: Dict[str, Tuple[int, int]]) -> Optional[float]:
        """Calculate body tilt angle"""
        required_points = ['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip']
        
        if not all(p in keypoints for p in required_points):
            return None
        
        shoulder_center = (
            (keypoints['left_shoulder'][0] + keypoints['right_shoulder'][0]) // 2,
            (keypoints['left_shoulder'][1] + keypoints['right_shoulder'][1]) // 2
        )
        
        hip_center = (
            (keypoints['left_hip'][0] + keypoints['right_hip'][0]) // 2,
            (keypoints['left_hip'][1] + keypoints['right_hip'][1]) // 2
        )
        
        angle = self.calculate_angle(shoulder_center, hip_center)
        
        return angle
    
    def calculate_aspect_ratio(self, keypoints: Dict[str, Tuple[int, int]]) -> Optional[float]:
        """Calculate body aspect ratio (width/height)"""
        if not keypoints:
            return None
        
        x_coords = [p[0] for p in keypoints.values()]
        y_coords = [p[1] for p in keypoints.values()]
        
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)
        
        if height == 0:
            return None
        
        return width / height
    
    def detect_fall(self, keypoints: Dict[str, Tuple[int, int]]) -> bool:
        """Detect fall using multi-criteria analysis"""
        if not keypoints:
            self.fall_frames_count = 0
            self.confidence_score = 0.0
            return False
        
        fall_score = 0.0
        max_score = 100.0
        
        body_angle = self.calculate_body_angle(keypoints)
        if body_angle is not None:
            self.angle_history.append(body_angle)
            
            if self.initial_check_frames < 15:
                self.initial_check_frames += 1
                if body_angle > self.max_initial_angle:
                    self.max_initial_angle = body_angle
            
            if body_angle < 30:
                fall_score += 40
            elif body_angle < 45:
                fall_score += 35
            elif body_angle < self.angle_threshold:
                fall_score += 25
        
        if len(self.angle_history) >= 3:
            angles = list(self.angle_history)
            if angles[-1] < angles[-2] < angles[-3]:
                fall_score += 15
            elif angles[-1] < angles[0]:
                fall_score += 10
        
        aspect_ratio = self.calculate_aspect_ratio(keypoints)
        if aspect_ratio is not None:
            self.aspect_ratio_history.append(aspect_ratio)
            
            if aspect_ratio > 2.0:
                fall_score += 25
            elif aspect_ratio > 1.5:
                fall_score += 20
            elif aspect_ratio > 1.2:
                fall_score += 10
        
        head_low = False
        head_very_low = False
        if 'nose' in keypoints:
            nose_y = keypoints['nose'][1]
            
            if 'left_ankle' in keypoints and 'right_ankle' in keypoints:
                avg_ankle_y = (keypoints['left_ankle'][1] + keypoints['right_ankle'][1]) / 2
                head_ankle_dist = abs(nose_y - avg_ankle_y)
                
                if head_ankle_dist < 150:
                    fall_score += 20
                    head_very_low = True
                elif head_ankle_dist < 250:
                    fall_score += 15
                    head_low = True
            
            if 'left_hip' in keypoints and 'right_hip' in keypoints:
                avg_hip_y = (keypoints['left_hip'][1] + keypoints['right_hip'][1]) / 2
                if nose_y > avg_hip_y:
                    fall_score += 20
                    head_very_low = True
        
        self.confidence_score = min(fall_score / max_score * 100, 100)
        
        fall_detected = self.confidence_score >= 60
        
        if self.initial_check_frames < 15:
            if self.max_initial_angle < 50:
                return False
        elif self.max_initial_angle < 50 and fall_detected:
            return False
        
        if fall_detected:
            self.fall_frames_count += 1
        else:
            self.fall_frames_count = max(0, self.fall_frames_count - 1)
        
        confirmed_fall = self.fall_frames_count >= 3
        
        if confirmed_fall and not self.is_fallen:
            self.is_fallen = True
            import time
            self.fall_start_time = time.time()
        elif not fall_detected and self.fall_frames_count == 0:
            self.is_fallen = False
        
        return confirmed_fall
    
    def get_fall_info(self) -> Dict:
        """Get fall status information"""
        info = {
            'is_fallen': self.is_fallen,
            'fall_start_time': self.fall_start_time,
            'duration': None
        }
        
        if self.is_fallen and self.fall_start_time:
            import time
            info['duration'] = time.time() - self.fall_start_time
        
        return info
    
    def get_confidence_score(self) -> float:
        """Get confidence score (0-100)"""
        return self.confidence_score
    
    def reset(self):
        """Reset state"""
        self.position_history.clear()
        self.is_fallen = False
        self.fall_start_time = None
        self.fall_frames_count = 0

