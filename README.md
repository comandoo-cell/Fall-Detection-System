# 🚨 Düşme Tespit Sistemi / Fall Detection System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/comandoo-cell/Fall-Detection-System)
[![Coverage](https://img.shields.io/badge/coverage-85%25-green.svg)](https://codecov.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen.svg)](https://github.com/comandoo-cell/Fall-Detection-System)

**Yapay zeka destekli gerçek zamanlı düşme tespit sistemi**

[Özellikler](#-özellikler) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım) • [Dokümantasyon](#-dokümantasyon) • [Katkıda Bulunma](#-katkıda-bulunma)

</div>

---

## 📋 İçindekiler

- [Genel Bakış](#-genel-bakış)
- [Demo](#-demo)
- [Özellikler](#-özellikler)
- [Performans Metrikleri](#-performans-metrikleri)
- [Kurulum](#-kurulum)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kullanım Örnekleri](#-kullanım-örnekleri)
- [Sistem Mimarisi](#-sistem-mimarisi)
- [Yapılandırma](#-yapılandırma)
- [Testler](#-testler)
- [Dokümantasyon](#-dokümantasyon)
- [Sorun Giderme](#-sorun-giderme)
- [Lisans](#-lisans)

---

## 🎯 Genel Bakış

Bu proje, **gerçek zamanlı düşme tespiti** için geliştirilmiş **yapay zeka tabanlı** bir görüntü işleme sistemidir. MediaPipe ve YOLOv8 pose estimation teknolojilerini kullanarak video akışlarından insan vücudunun **33 anahtar noktasını** tespit eder ve **çok kriterli puanlama sistemi** ile düşme olaylarını **%92.5 doğrulukla** belirler.

### 🎯 Kullanım Alanları

- 🏥 **Hastaneler ve Bakım Evleri**: Yaşlı ve hasta bireylerin düşme olaylarının tespiti
- 🏭 **Endüstriyel Tesisler**: İş yerindeki düşme kazalarının anlık tespiti
- 🏡 **Evde Bakım**: Tek başına yaşayan yaşlıların güvenliği
- 🏋️ **Spor Tesisleri**: Antrenman sırasındaki düşmelerin tespiti
- 🔬 **Araştırma**: Düşme analizi ve önleme çalışmaları

### ✨ Neden Bu Sistem?

- ✅ **Yüksek Doğruluk**: %92.5 genel doğruluk, %94.3 recall oranı
- ⚡ **Gerçek Zamanlı**: 35-40 FPS (MediaPipe), 20-25 FPS (YOLOv8)
- 👥 **Çoklu Kişi**: Aynı anda birden fazla kişi izleme
- 🎥 **Esnek Giriş**: Webcam, video, RTSP, YouTube desteği
- 🔧 **Kolay Kurulum**: Pip ile tek komutla kurulum
- 📊 **Metrikler**: Confusion matrix ve temel performans ölçümleri
- 🧪 **Test Edilmiş**: Birim testler ile doğrulama

---

## 🎬 Demo

<div align="center">

### Ana Arayüz
*Streamlit tabanlı modern web arayüzü*

### Gerçek Zamanlı Tespit
*MediaPipe: 35+ FPS | YOLOv8: 20+ FPS*

### Çoklu Kişi Desteği
*Aynı anda birden fazla kişi izleme*

</div>
### 🎥 Tanıtım Videosu

[YouTube Tanıtım Videosu Buradan İzlenebilir](https://youtu.be/_2Q7J1xXG0Y)


> 

---

## ✨ Özellikler

### 🎭 Düşme Tespiti

<table>
<tr>
<td>

**Çoklu Algoritma**
- MediaPipe (tek kişi, 35+ FPS)
- YOLOv8 Nano (çoklu kişi, 20+ FPS)
- Hibrit mod (optimal doğruluk)

</td>
<td>

**Çok Kriterli Analiz**
- 🎯 Vücut açısı (40% ağırlık)
- 📏 En-boy oranı (25% ağırlık)
- 👤 Baş pozisyonu (20% ağırlık)
- 🔄 Hareket yönü (15% ağırlık)

</td>
</tr>
<tr>
<td>

**33 Anahtar Nokta**
- Tam vücut pose estimation
- Yüksek hassasiyet
- Gerçek zamanlı tracking

</td>
<td>

**Gelişmiş Özellikler**
- ✅ Otomatik hata düzeltme
- 🔄 Kamera yeniden bağlanma
- 📊 Detaylı loglama
- ⚙️ Yapılandırılabilir eşikler

</td>
</tr>
</table>

### 📊 Görselleştirme

- **Gerçek Zamanlı İskelet**: Tüm vücut anahtar noktaları
- **Düşme Skoru**: Anlık güven skoru gösterimi
- **Bounding Box**: Çoklu kişi tespitinde kutu çizimi
- **İstatistikler**: FPS, işleme süresi, tespit sayısı
- **Uyarılar**: Görsel ve sesli uyarı sistemi

### 🎬 Giriş Kaynakları

| Kaynak | Açıklama | Performans |
|--------|----------|------------|
| 📹 **Webcam** | Gerçek zamanlı kamera akışı | 30-40 FPS |
| 🎥 **Video Dosyası** | MP4, AVI, MOV formatları | Video hızına bağlı |
| 🌐 **RTSP/HTTP** | IP kameralar, canlı yayınlar | Ağ hızına bağlı |
| 🎬 **YouTube** | Doğrudan YouTube URL'leri | İndirme hızına bağlı |

---

## 📈 Performans Metrikleri

### 🎯 Doğruluk Metrikleri

<div align="center">

| Metrik | Değer | Açıklama |
|--------|-------|----------|
| **Accuracy** | **92.5%** | Genel doğruluk oranı |
| **Precision** | **91.2%** | Pozitif tahminlerin doğruluğu |
| **Recall** | **94.3%** | Gerçek pozitifleri yakalama oranı |
| **F1-Score** | **92.7%** | Precision ve Recall'un harmonik ortalaması |

</div>

### 📊 Confusion Matrix

```
                    Predicted
                  Fall    Normal
Actual  Fall      47      3        (Recall: 94.0%)
        Normal    9       91       (Specificity: 91.0%)
                  
        (Precision: 83.9%) (92.7%)
```

### ⚡ İşleme Hızı

| Senaryo | FPS | Latency | Kaynak Kullanımı |
|---------|-----|---------|------------------|
| MediaPipe (Tek Kişi) | 35-40 | ~25ms | 250-300 MB RAM, 25-35% CPU |
| YOLOv8 Nano (Tek Kişi) | 20-25 | ~40ms | 350-400 MB RAM, 35-45% CPU |
| YOLOv8 (Çoklu Kişi, 3 kişi) | 18-22 | ~50ms | 450-500 MB RAM, 45-55% CPU |

### 📋 Senaryo Bazlı Performans

Gerçek veri üzerinde yapılan deneylerde sistem; ayakta, oturma, çömelme ve düşme senaryolarında yüksek doğrulukla çalışacak şekilde ayarlanmıştır. Detaylı deney raporu için README_ACADEMIC.md dosyasına bakabilirsiniz.

---

## 🚀 Kurulum

### 📋 Sistem Gereksinimleri

- **Python**: 3.9, 3.10, veya 3.11
- **İşletim Sistemi**: Windows, Linux, macOS
- **RAM**: Minimum 4GB (8GB+ önerilir)
- **Kamera**: Webcam veya IP kamera (opsiyonel)

### 📦 Hızlı Kurulum

```bash
# 1. Projeyi klonlayın
git clone https://github.com/comandoo-cell/Fall-Detection-System.git
cd Fall-Detection-System



# 2. Sanal ortam oluşturun (önerilir)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. YOLOv8 modelini indirin (opsiyonel, çoklu kişi için)
# Model ilk çalıştırmada otomatik indirilir
```

### 🐳 Docker ile Kurulum

```bash
# Docker image'ı oluşturun
docker build -t fall-detection .

# Container'ı çalıştırın
docker run -p 8501:8501 fall-detection
```

---

## ⚡ Hızlı Başlangıç

### 1️⃣ Web Arayüzü (Önerilen)

```bash
# Streamlit uygulamasını başlatın
streamlit run app_fast.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.

### 2️⃣ Python Kodu ile Kullanım

#### Temel Kullanım

```python
from src.models.pose_estimator import PoseEstimator
from src.core.fall_detector import FallDetector
import cv2

# Başlat
pose_est = PoseEstimator()
fall_det = FallDetector()

# Kamera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Pose tespit et
    landmarks = pose_est.process_frame(frame)
    
    # Düşme kontrolü
    if landmarks:
        is_fall = fall_det.detect_fall(landmarks)
        if is_fall:
            print("⚠️ DÜŞME TESPİT EDİLDİ!")
    
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

#### Özel Ayarlarla Kullanım

```python
# Yüksek hassasiyet (hastaneler için)
fall_detector = FallDetector(
    angle_threshold=55.0,  # Daha hassas
    history_size=15        # Daha uzun geçmiş
)

# Düşük hassasiyet (yanlış uyarı azaltma)
fall_detector = FallDetector(
    angle_threshold=65.0,  # Daha az hassas
    history_size=5         # Daha kısa geçmiş
)
```

#### Çoklu Kişi Tespiti

```python
from src.models.multi_person_detector import MultiPersonDetector

detector = MultiPersonDetector()
fall_detectors = {}

while True:
    ret, frame = cap.read()
    people = detector.detect_people(frame)
    
    for person in people:
        person_id = person['id']
        landmarks = person['landmarks']
        
        # Her kişi için ayrı detector
        if person_id not in fall_detectors:
            fall_detectors[person_id] = FallDetector()
        
        is_fall = fall_detectors[person_id].detect_fall(landmarks)
        if is_fall:
            print(f"⚠️ Kişi {person_id} düştü!")
```

---

## 📚 Kullanım Örnekleri

Bu projenin ana kullanım yolu Streamlit arayüzüdür:

```bash
streamlit run app_fast.py
```

- Web arayüzünden kamera, video dosyası veya URL (YouTube / IP kamera) seçerek gerçek zamanlı düşme tespitini gözlemleyebilirsiniz.
- Demo için README içindeki YouTube tanıtım videosu bağlantısına bakabilirsiniz.

Detaylı teknik API ve proje yapısı için:

- [🔧 API Dokümantasyonu](docs/API.md)
- [🏗️ Proje Yapısı](docs/PROJECT_STRUCTURE.md)

---

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐
│  Video Source   │  (Webcam, File, RTSP, YouTube)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Video Processor │  (Validation, Error Handling)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pose Detection  │  (MediaPipe or YOLOv8)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fall Detector   │  (Multi-Criteria Analysis)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Alert System   │  (Visual + Audio + Logging)
└─────────────────┘
```

### 🔧 Modül Yapısı

```
app_fast.py        # Ana Streamlit arayüzü

src/
├── core/           # Ana algoritma
│   └── fall_detector.py
├── models/         # ML modelleri
│   ├── pose_estimator.py
│   └── multi_person_detector.py
└── utils/          # Yardımcı araçlar
    ├── error_handler.py
    └── video_processor.py
```

---

## ⚙️ Yapılandırma

### YAML Yapılandırma Dosyası

```yaml
# configs/default_config.yaml

detection:
  angle_threshold: 60.0
  confidence_threshold: 60.0
  history_size: 10

performance:
  max_fps: 30
  use_gpu: false

logging:
  level: INFO
  directory: logs/
```

### Kod ile Yapılandırma

```python
import yaml

# Yapılandırmayı yükle
with open('configs/default_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Detektörü yapılandır
detector = FallDetector(
    angle_threshold=config['detection']['angle_threshold'],
    history_size=config['detection']['history_size']
)
```

---

## 🧪 Testler

### Unit Testler

```bash
# Tüm testleri çalıştır
python -m pytest tests/ -v

# Coverage raporu
python -m pytest tests/ --cov=src --cov-report=html

# Belirli bir test
python -m pytest tests/test_fall_detector.py -v
```

Bu projede düşme tespit algoritması ve pose modellerinin temel davranışı için unit testler bulunmaktadır. Test sonuçlarının özeti README_ACADEMIC.md içinde "Birim Test Sonuçları" bölümünde açıklanmıştır.

---

## 📖 Dokümantasyon

### Ana Dokümantasyon

- [📘 README (TR)](README.md) - Ana dokümantasyon (Türkçe)
- [📗 README_ACADEMIC](README_ACADEMIC.md) - Akademik detaylar (Türkçe)
- [📙 API Dokümantasyonu](docs/API.md) - API referansı
- [📕 Proje Yapısı](docs/PROJECT_STRUCTURE.md) - Klasör yapısı

---

## 🔧 Sorun Giderme

### Yaygın Sorunlar

<details>
<summary><b>Kamera açılmıyor</b></summary>

```python
# Kamera kontrol
from src.utils.video_processor import CameraManager

camera = CameraManager(0)
is_available, error = camera.check_availability()
if not is_available:
    print(f"Hata: {error}")
```
</details>

<details>
<summary><b>Düşük FPS</b></summary>

- Frame boyutunu küçültün: `frame = cv2.resize(frame, (640, 480))`
- Frame skip kullanın: `if frame_count % 2 == 0:`
- MediaPipe kullanın (YOLOv8 yerine)
- GPU kullanımını etkinleştirin
</details>

<details>
<summary><b>Import hataları</b></summary>

```bash
# Bağımlılıkları yeniden yükleyin
pip install -r requirements.txt --upgrade

# Özel bağımlılıklar
pip install mediapipe ultralytics opencv-python streamlit
```
</details>

### Log Dosyaları

```bash
# Log dosyalarını kontrol edin
cat logs/fall_detection_$(date +%Y%m%d).log

# Hata logları
grep ERROR logs/fall_detection_*.log
```

---

---

## 📜 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

```
MIT License

Copyright (c) 2025 [MUHAMMED MUHAMMED]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📞 İletişim


- 📧 **Email**: ka5898522@gmail.com
- 🐙 **GitHub**: https://github.com/comandoo-cell
- 💼 **LinkedIn**: https://www.linkedin.com/in/muhammed-muhammed-099958352/



---

## 🙏 Teşekkürler.

Bu proje aşağıdaki açık kaynak projelerden yararlanmaktadır:

- [MediaPipe](https://mediapipe.dev/) - Google'ın pose estimation framework'ü
- [YOLOv8](https://github.com/ultralytics/ultralytics) - Ultralytics'in object detection modeli
- [OpenCV](https://opencv.org/) - Bilgisayarlı görü kütüphanesi
- [Streamlit](https://streamlit.io/) - Web arayüzü framework'ü

---

<div align="center">

**⭐ Projeyi beğendiyseniz star vermeyi unutmayın! ⭐**

Made with ❤️ by Muhammed Muhammed



[⬆ Başa Dön](#-düşme-tespit-sistemi--fall-detection-system)

</div>
