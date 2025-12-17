# API Documentation

## Core Modules API Reference

### FallDetector Class

#### Constructor
```python
FallDetector(
    angle_threshold: float = 60.0,
    history_size: int = 10
)
```

**Parameters:**
- `angle_threshold`: Body angle threshold for fall detection (degrees)
- `history_size`: Number of frames to keep in history

#### Methods

##### detect_fall()
```python
def detect_fall(
    keypoints: Dict[str, Tuple[int, int]]
) -> bool
```

Detect fall from pose keypoints.

**Parameters:**
- `keypoints`: Dictionary of body landmarks with (x, y) coordinates

**Returns:**
- `bool`: True if fall detected, False otherwise

**Example:**
```python
detector = FallDetector()
is_fall = detector.detect_fall(keypoints)
if is_fall:
    print("Fall detected!")
```

##### calculate_body_angle()
```python
def calculate_body_angle(
    keypoints: Dict[str, Tuple[int, int]]
) -> Optional[float]
```

Calculate body tilt angle.

**Returns:**
- `float`: Angle in degrees (0-90)
- `None`: If insufficient keypoints

---

### PoseEstimator Class

#### Constructor
```python
PoseEstimator()
```

Initialize MediaPipe pose estimator.

#### Methods

##### process_frame()
```python
def process_frame(
    frame: np.ndarray
) -> Optional[Dict[str, Tuple[int, int]]]
```

Process frame and extract pose landmarks.

**Parameters:**
- `frame`: RGB/BGR image (numpy array)

**Returns:**
- `Dict`: Landmark dictionary with body parts
- `None`: If no person detected

**Example:**
```python
estimator = PoseEstimator()
landmarks = estimator.process_frame(frame)
```

---

### MultiPersonDetector Class

#### Constructor
```python
MultiPersonDetector(model_path: str = "yolov8n-pose.pt")
```

Initialize YOLOv8 multi-person detector.

**Parameters:**
- `model_path`: Path to YOLOv8 model file

#### Methods

##### detect_people()
```python
def detect_people(
    frame: np.ndarray
) -> List[Tuple[int, Dict[str, Tuple[int, int]]]]
```

Detect multiple people in frame.

**Returns:**
- `List`: List of (person_id, landmarks) tuples

**Example:**
```python
detector = MultiPersonDetector()
people = detector.detect_people(frame)
for person_id, landmarks in people:
    print(f"Person {person_id} detected")
```

---

### ErrorHandler Class

#### Methods

##### log_error()
```python
def log_error(
    message: str,
    exception: Optional[Exception] = None
)
```

Log error with optional exception details.

**Example:**
```python
from src.error_handler import error_handler

try:
    # some operation
    pass
except Exception as e:
    error_handler.log_error("Operation failed", e)
```

---

### VideoProcessor Class

#### Methods

##### validate_frame()
```python
def validate_frame(
    frame: np.ndarray
) -> Tuple[bool, Optional[str]]
```

Validate frame quality.

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

##### process_frame_safe()
```python
def process_frame_safe(
    frame: np.ndarray,
    processor_func: callable,
    *args, **kwargs
) -> Tuple[bool, any, Optional[str]]
```

Safely process frame with error handling.

**Returns:**
- `Tuple`: (success, result, error_message)

---

## Usage Examples

### Basic Fall Detection

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
    
    # Display
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Multi-Person Detection

```python
from src.multi_person_detector import MultiPersonDetector
from src.fall_detector import FallDetector

# Initialize
multi_det = MultiPersonDetector()
fall_det = FallDetector()

# Process frame
people = multi_det.detect_people(frame)

for person_id, landmarks in people:
    is_fall = fall_det.detect_fall(landmarks)
    if is_fall:
        print(f"Person {person_id} has fallen!")
```

### Custom Configuration

```python
# High sensitivity for hospitals
detector = FallDetector(
    angle_threshold=55.0,  # Lower = more sensitive
    history_size=15        # Longer history
)

# Low sensitivity to reduce false alarms
detector = FallDetector(
    angle_threshold=65.0,  # Higher = less sensitive
    history_size=5         # Shorter history
)
```

### Error Handling

```python
from src.error_handler import error_handler
from src.video_processor import VideoProcessor

processor = VideoProcessor()

# Check camera availability
is_available, error_msg = processor.check_camera_available(0)
if not is_available:
    print(error_msg)
    error_handler.log_error("Camera not available")

# Validate frame
is_valid, error_msg = processor.validate_frame(frame)
if not is_valid:
    error_handler.log_warning(f"Invalid frame: {error_msg}")

# Safe processing
success, result, error = processor.process_frame_safe(
    frame,
    pose_estimator.process_frame
)

if not success:
    error_handler.log_error(f"Processing failed: {error}")
```

---

## Configuration API

### YAML Configuration

```yaml
# config.yaml
detection:
  angle_threshold: 60.0
  confidence_threshold: 60.0
  velocity_threshold: 0.5
  history_size: 10

performance:
  max_fps: 30
  use_gpu: false
  buffer_size: 1

logging:
  level: INFO
  directory: logs/
  max_file_size: 10MB
  max_files: 30
```

### Loading Configuration

```python
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

detector = FallDetector(
    angle_threshold=config['detection']['angle_threshold'],
    history_size=config['detection']['history_size']
)
```

---

## Return Types and Data Structures

### Landmarks Dictionary
```python
{
    'nose': (x, y),
    'left_eye': (x, y),
    'right_eye': (x, y),
    'left_ear': (x, y),
    'right_ear': (x, y),
    'left_shoulder': (x, y),
    'right_shoulder': (x, y),
    'left_elbow': (x, y),
    'right_elbow': (x, y),
    'left_wrist': (x, y),
    'right_wrist': (x, y),
    'left_hip': (x, y),
    'right_hip': (x, y),
    'left_knee': (x, y),
    'right_knee': (x, y),
    'left_ankle': (x, y),
    'right_ankle': (x, y)
}
```

### Detection Result
```python
{
    'is_fall': bool,
    'confidence': float,  # 0-100
    'body_angle': float,  # degrees
    'aspect_ratio': float,
    'timestamp': datetime
}
```

---

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| CAM_001 | Camera not accessible | Camera device not found |
| CAM_002 | Camera read failed | Cannot read frames from camera |
| PROC_001 | Invalid frame | Frame validation failed |
| PROC_002 | Processing error | Error during frame processing |
| MODEL_001 | Model load failed | Cannot load ML model |
| MODEL_002 | Inference error | Error during model inference |

---

## Performance Considerations

### Optimization Tips

1. **Use GPU when available**
```python
# Check GPU availability
import torch
use_gpu = torch.cuda.is_available()
```

2. **Reduce frame resolution**
```python
frame = cv2.resize(frame, (640, 480))
```

3. **Skip frames**
```python
frame_skip = 2  # Process every 2nd frame
if frame_count % frame_skip == 0:
    process_frame(frame)
```

4. **Use MediaPipe for single person**
- Faster than YOLOv8
- 35-40 FPS vs 20-25 FPS

---

## Thread Safety

**Note**: Current implementation is **not** thread-safe.

For multi-threaded usage:
```python
import threading

class ThreadSafeFallDetector:
    def __init__(self):
        self.detector = FallDetector()
        self.lock = threading.Lock()
    
    def detect_fall(self, keypoints):
        with self.lock:
            return self.detector.detect_fall(keypoints)
```

---

## Version Compatibility

- **Python**: 3.9, 3.10, 3.11
- **OpenCV**: >= 4.8.0
- **MediaPipe**: >= 0.10.0
- **Ultralytics**: >= 8.0.0
- **Streamlit**: >= 1.28.0

---

For more examples, see [examples/README.md](../examples/README.md)
