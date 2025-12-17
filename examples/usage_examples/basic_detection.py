"""
Basic Fall Detection Example
============================

This example demonstrates the most basic usage of the fall detection system.
"""

import cv2
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from src.models.pose_estimator import PoseEstimator
from src.core.fall_detector import FallDetector

def main():
    """Run basic fall detection"""
    
    # Initialize components
    print("Initializing fall detection system...")
    pose_estimator = PoseEstimator()
    fall_detector = FallDetector()
    
    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("System ready. Press 'q' to quit.")
    
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Detect pose
        landmarks = pose_estimator.process_frame(frame)
        
        # Check for fall
        if landmarks:
            is_fall = fall_detector.detect_fall(landmarks)
            
            # Display result
            if is_fall:
                cv2.putText(frame, "FALL DETECTED!", (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                print("⚠️ FALL DETECTED!")
            else:
                cv2.putText(frame, "Normal", (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No person detected", (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
        # Show frame
        cv2.imshow('Fall Detection', frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("System stopped.")

if __name__ == "__main__":
    main()
