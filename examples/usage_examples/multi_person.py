"""
Multi-Person Detection Example
==============================

This example demonstrates detecting falls for multiple people simultaneously.
"""

import cv2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from src.models.multi_person_detector import MultiPersonDetector
from src.core.fall_detector import FallDetector

def main():
    """Run multi-person fall detection"""
    
    # Initialize
    print("Initializing multi-person fall detection...")
    detector = MultiPersonDetector(
        model_name='yolov8n-pose.pt',
        confidence=0.5
    )
    
    # Create separate fall detector for each person
    fall_detectors = {}
    
    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Multi-person detection active. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect all people
        people = detector.detect_people(frame)
        
        # Process each person
        for person_data in people:
            person_id = person_data.get('id', 0)
            landmarks = person_data.get('landmarks')
            bbox = person_data.get('bbox')
            
            if landmarks:
                # Create detector for new person
                if person_id not in fall_detectors:
                    fall_detectors[person_id] = FallDetector()
                
                # Check for fall
                is_fall = fall_detectors[person_id].detect_fall(landmarks)
                
                # Draw bounding box
                if bbox:
                    x1, y1, x2, y2 = map(int, bbox)
                    color = (0, 0, 255) if is_fall else (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Add label
                    label = f"Person {person_id}: {'FALL!' if is_fall else 'OK'}"
                    cv2.putText(frame, label, (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    
                    if is_fall:
                        print(f"⚠️ Person {person_id} has fallen!")
        
        # Show info
        cv2.putText(frame, f"People detected: {len(people)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.imshow('Multi-Person Fall Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("System stopped.")

if __name__ == "__main__":
    main()
