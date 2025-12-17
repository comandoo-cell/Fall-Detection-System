# API Dokümantasyonu

## Çekirdek Modüller API Referansı

### FallDetector Sınıfı

#### Kurucu (Constructor)
```python
FallDetector(
    angle_threshold: float = 60.0,
    history_size: int = 10
)
```

**Parametreler:**
- `angle_threshold`: Düşme tespiti için vücut açısı eşiği (derece)
- `history_size`: Geçmişte tutulacak kare sayısı

#### Metotlar

##### detect_fall()
```python
def detect_fall(
    keypoints: Dict[str, Tuple[int, int]]
) -> bool
```

Anahtar noktalardan düşme tespiti yapar.

**Parametreler:**
- `keypoints`: Vücut landmark'larının (x, y) koordinatlarını içeren sözlük

**Dönüş:**
- `bool`: Düşme tespit edildiyse `True`, edilmediyse `False`

**Örnek:**
```python
detector = FallDetector()
is_fall = detector.detect_fall(keypoints)
if is_fall:
    print("Dusme tespit edildi!")
```

##### calculate_body_angle()
```python
def calculate_body_angle(
    keypoints: Dict[str, Tuple[int, int]]
) -> Optional[float]
```

Vücut eğim açısını hesaplar.

**Dönüş:**
- `float`: Derece cinsinden açı (0-90)
- `None`: Yeterli anahtar nokta yoksa

---

### PoseEstimator Sınıfı

#### Kurucu (Constructor)
```python
PoseEstimator()
```

MediaPipe tabanlı pose (duruş) tahmincisini başlatır.

#### Metotlar

##### process_frame()
```python
def process_frame(
    frame: np.ndarray
) -> Optional[Dict[str, Tuple[int, int]]]
```

Bir kareyi işler ve pose landmark'larını çıkarır.

**Parametreler:**
- `frame`: RGB/BGR görüntü (numpy array)

**Dönüş:**
- `Dict`: Vücut parçalarını içeren landmark sözlüğü
- `None`: Eğer kişi tespit edilmezse

**Örnek:**
```python
estimator = PoseEstimator()
landmarks = estimator.process_frame(frame)
```

---

### MultiPersonDetector Sınıfı

#### Kurucu (Constructor)
```python
MultiPersonDetector(model_path: str = "yolov8n-pose.pt")
```

YOLOv8 tabanlı çoklu kişi pose dedektörünü başlatır.

**Parametreler:**
- `model_path`: YOLOv8 model dosyasının yolu

#### Metotlar

##### detect_people()
```python
def detect_people(
    frame: np.ndarray
) -> List[Tuple[int, Dict[str, Tuple[int, int]]]]
```

Bir karedeki birden fazla kişiyi tespit eder.

**Dönüş:**
- `List`: Her bir kişi için `(person_id, landmarks)` tuple listesi

## Kullanım Örnekleri

### Temel Düşme Tespiti

```python
from src.pose_estimator import PoseEstimator
from src.fall_detector import FallDetector
import cv2


pose_est = PoseEstimator()
fall_det = FallDetector()


cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    
    landmarks = pose_est.process_frame(frame)
    
    
    if landmarks:
        is_fall = fall_det.detect_fall(landmarks)
        if is_fall:
            print("⚠️ DUSME TESPIT EDILDI!")
    
    
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Coklu Kisi Tespiti

```python
from src.multi_person_detector import MultiPersonDetector
from src.fall_detector import FallDetector


multi_det = MultiPersonDetector()
fall_det = FallDetector()


people = multi_det.detect_people(frame)

for person_id, landmarks in people:
    is_fall = fall_det.detect_fall(landmarks)
    if is_fall:
        print(f"Kisi {person_id} dustu!")
```

### Ozellestirilmis Ayarlar

```python

| CAM_001 | Camera not accessible | Camera device not found |
    angle_threshold=55.0,  
    history_size=15        
)


| CAM_002 | Camera read failed | Cannot read frames from camera |
    angle_threshold=65.0,  
    history_size=5         
)
```

### Hata Yönetimi

```python
from src.error_handler import error_handler
from src.video_processor import VideoProcessor

processor = VideoProcessor()


is_available, error_msg = processor.check_camera_available(0)
if not is_available:
    print(error_msg)
    error_handler.log_error("Kamera kullanilamiyor")


is_valid, error_msg = processor.validate_frame(frame)
if not is_valid:
    error_handler.log_warning(f"Gecersiz kare: {error_msg}")


success, result, error = processor.process_frame_safe(
    frame,
    pose_estimator.process_frame
)

if not success:
    error_handler.log_error(f"Isleme basarisiz: {error}")
```

---

## Yapılandırma API'si

### YAML Yapılandırması

```yaml

| PROC_001 | Invalid frame | Frame validation failed |
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

### Yapılandırmayı Yükleme

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

## Dönüş Tipleri ve Veri Yapıları

### Landmarks Sözlüğü
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

### Tespit Sonucu
```python
{
    'is_fall': bool,
    'confidence': float,  # 0-100
    'body_angle': float,  # derece
    'aspect_ratio': float,
    'timestamp': datetime
}
```

---

## Hata Kodları

| Kod | Mesaj | Açıklama |
|------|-------|----------|
| CAM_001 | Kamera erisilemiyor | Kamera cihazı bulunamadi |
| CAM_002 | Kamera okuma hatasi | Kameradan kare okunamadi |
| PROC_001 | Gecersiz kare | Kare dogrulama basarisiz |
| PROC_002 | Isleme hatasi | Kare islenirken hata olustu |
| MODEL_001 | Model yuklenemedi | ML modeli yuklenemiyor |
| MODEL_002 | Inference hatasi | Model calistirilirken hata olustu |

---

## Performans Notları

### Optimizasyon Ipuçları

1. **Mümkünse GPU kullanin**
```python

import torch
use_gpu = torch.cuda.is_available()
```

2. **Kare çözünürlüğünü düşürün**
```python
frame = cv2.resize(frame, (640, 480))
```

3. **Kare atlayin (frame skip)**
```python
frame_skip = 2  
if frame_count % frame_skip == 0:
    process_frame(frame)
```

4. **Tek kişi için MediaPipe kullanin**
- YOLOv8'den daha hizlidir
- 35-40 FPS vs 20-25 FPS

---

## Thread Safety (Çoklu İş Parçacığı Güvenliği)

**Not**: Mevcut implementasyon **thread-safe degildir**.

Çoklu thread'li kullanim icin:
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

## Sürüm Uyumluluğu

- **Python**: 3.9, 3.10, 3.11
- **OpenCV**: >= 4.8.0
- **MediaPipe**: >= 0.10.0
- **Ultralytics**: >= 8.0.0
- **Streamlit**: >= 1.28.0

---

| PROC_002 | Processing error | Error during frame processing |
| MODEL_001 | Model load failed | Cannot load ML model |
| MODEL_002 | Inference error | Error during model inference |

---

## Performance Considerations

### Optimization Tips

1. **Use GPU when available**
```python

import torch
use_gpu = torch.cuda.is_available()
```

2. **Reduce frame resolution**
```python
frame = cv2.resize(frame, (640, 480))
```

3. **Skip frames**
```python
frame_skip = 2  
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

Ek örnek kullanım senaryoları için README.md ve README_ACADEMIC.md dosyalarına bakabilirsiniz.
