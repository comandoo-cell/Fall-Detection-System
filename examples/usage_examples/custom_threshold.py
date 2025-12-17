"""
Custom Threshold Example
========================

This example shows how to customize detection thresholds.
"""

import cv2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from src.models.pose_estimator import PoseEstimator
from src.core.fall_detector import FallDetector

def main():
    """Run fall detection with custom thresholds"""
    
    # Initialize with custom settings
    print("Initializing with custom thresholds...")
    pose_estimator = PoseEstimator(
        min_detection_confidence=0.7,  # Higher confidence
        min_tracking_confidence=0.7
    )
    
    # High sensitivity (good for hospitals/elderly care)
    fall_detector = FallDetector(
        angle_threshold=55.0,  # Lower = more sensitive
        history_size=15        # Longer history
    )
    
    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("High sensitivity mode activated.")
    print("Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process frame
        landmarks = pose_estimator.process_frame(frame)
        
        if landmarks:
            is_fall = fall_detector.detect_fall(landmarks)
            confidence = fall_detector.get_confidence()
            
            # Display with confidence
            if is_fall:
                text = f"FALL! Confidence: {confidence:.1f}%"
                cv2.putText(frame, text, (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                print(f"⚠️ {text}")
            else:
                text = f"Normal (Confidence: {confidence:.1f}%)"
                cv2.putText(frame, text, (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Fall Detection - High Sensitivity', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
