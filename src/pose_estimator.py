"""
Pose Estimation Module
======================"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, Tuple, List


class PoseEstimator:
    """Pose Estimator using MediaPipe"""
    
    # تعريف أسماء نقاط المفاصل المهمة
    NOSE = 0
    LEFT_EYE = 2
    RIGHT_EYE = 5
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    
    def __init__(self, min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """Initialize pose estimator"""
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            model_complexity=1
        )
        
        self.results = None
    
    def process_frame(self, frame: np.ndarray) -> bool:
        """Process frame and extract keypoints"""
        self.results = self.pose.process(frame)
        
        return self.results is not None and self.results.pose_landmarks is not None
    
    def get_landmarks(self) -> Optional[List]:
        """Get keypoints"""
        if self.results and self.results.pose_landmarks:
            return self.results.pose_landmarks.landmark
        return None
    
    def get_landmark_coordinates(self, landmark_id: int, 
                                 frame_width: int, 
                                 frame_height: int) -> Optional[Tuple[int, int]]:
        """Get coordinates of specific landmark"""
        landmarks = self.get_landmarks()
        if landmarks is None or landmark_id >= len(landmarks):
            return None
        
        landmark = landmarks[landmark_id]
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        
        return (x, y)
    
    def get_all_keypoints(self, frame_width: int, 
                         frame_height: int) -> Dict[str, Tuple[int, int]]:
        """Get all important keypoints for fall detection"""
        keypoints = {}
        
        landmarks = self.get_landmarks()
        if landmarks is None:
            return keypoints
        
        important_points = {
            'nose': self.NOSE,
            'left_shoulder': self.LEFT_SHOULDER,
            'right_shoulder': self.RIGHT_SHOULDER,
            'left_hip': self.LEFT_HIP,
            'right_hip': self.RIGHT_HIP,
            'left_knee': self.LEFT_KNEE,
            'right_knee': self.RIGHT_KNEE,
            'left_ankle': self.LEFT_ANKLE,
            'right_ankle': self.RIGHT_ANKLE
        }
        
        for name, idx in important_points.items():
            coords = self.get_landmark_coordinates(idx, frame_width, frame_height)
            if coords is not None:
                keypoints[name] = coords
        
        return keypoints
    
    def draw_skeleton(self, frame: np.ndarray) -> np.ndarray:
        """Draw skeleton on frame"""
        if self.results and self.results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                self.results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        return frame
    
    def draw_keypoints(self, frame: np.ndarray, 
                      keypoints: Dict[str, Tuple[int, int]],
                      color: Tuple[int, int, int] = (0, 255, 0),
                      radius: int = 5) -> np.ndarray:
        """Draw keypoints on frame"""
        for name, (x, y) in keypoints.items():
            cv2.circle(frame, (x, y), radius, color, -1)
            cv2.putText(frame, name, (x + 10, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        return frame
    
    def calculate_center_of_mass(self, keypoints: Dict[str, Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """Calculate center of mass from keypoints"""
        if not keypoints:
            return None
        
        trunk_points = ['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip']
        
        valid_points = [keypoints[p] for p in trunk_points if p in keypoints]
        
        if not valid_points:
            return None
        
        x_avg = int(sum(p[0] for p in valid_points) / len(valid_points))
        y_avg = int(sum(p[1] for p in valid_points) / len(valid_points))
        
        return (x_avg, y_avg)
    
    def close(self):
        """Close and release resources"""
        if self.pose and hasattr(self.pose, '_graph') and self.pose._graph is not None:
            self.pose.close()
    
    def __del__(self):
        """Cleanup resources"""
        try:
            self.close()
        except:
            pass

