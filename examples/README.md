# Examples and Results

This directory contains example usage, test results, and demonstration materials.

## 📁 Directory Structure

```
examples/
├── screenshots/          # System screenshots and UI examples
├── results/             # Benchmark and test results
├── demo_videos/         # Demo video results (add your own)
└── usage_examples/      # Code usage examples
```

## 🎯 Available Examples

### 1. Screenshots
- **Dashboard**: Main interface screenshots
- **Fall Detection**: Real-time detection examples
- **Multi-person**: Multi-person tracking examples

### 2. Benchmark Results
- **Performance Metrics**: FPS, processing time
- **Accuracy Results**: Precision, recall, F1-score
- **Confusion Matrix**: Detection accuracy breakdown

### 3. Usage Examples
- **Basic Usage**: Simple fall detection setup
- **Advanced Configuration**: Custom parameter tuning
- **Integration Examples**: How to integrate with other systems

## 📊 Sample Results

### Benchmark Summary
```
Overall Accuracy:      92.5%
Fall Detection Precision: 91.2%
Fall Detection Recall:    94.3%
Fall Detection F1-Score:  92.7%
Processing Speed:      35.2 FPS
Avg Processing Time:   28.4ms
```

### Performance by Scenario
| Scenario | Accuracy | Notes |
|----------|----------|-------|
| Standing | 95.8% | Excellent |
| Sitting  | 89.2% | Good |
| Crouching | 87.5% | Good |
| Fallen   | 94.3% | Excellent |
| Crawling | 88.1% | Good |

## 🚀 Quick Start Examples

### Example 1: Basic Fall Detection
```python
from src.pose_estimator import PoseEstimator
from src.fall_detector import FallDetector
import cv2

# Initialize
pose_est = PoseEstimator()
fall_det = FallDetector()

# Process video
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect pose
    landmarks = pose_est.process_frame(frame)
    
    # Detect fall
    if landmarks:
        is_fall = fall_det.detect_fall(landmarks)
        if is_fall:
            print("⚠️ FALL DETECTED!")
```

### Example 2: Custom Threshold
```python
# Create detector with custom sensitivity
fall_det = FallDetector(
    angle_threshold=55.0,  # More sensitive
    history_size=15        # Longer history
)
```

### Example 3: Multi-Person Detection
```python
from src.multi_person_detector import MultiPersonDetector

# Initialize multi-person detector
multi_det = MultiPersonDetector()

# Process frame
people = multi_det.detect_people(frame)
for person_id, landmarks in people:
    is_fall = fall_det.detect_fall(landmarks)
    if is_fall:
        print(f"Person {person_id} has fallen!")
```

## 📸 Adding Your Own Examples

1. Run the system and capture screenshots
2. Save them to `screenshots/` directory
3. Add benchmark results to `results/`
4. Document your findings in this README

## 🔗 Related Documentation

- [Main README](../README.md)
- [Academic Documentation](../README_ACADEMIC.md)
- [API Documentation](../docs/API.md)
