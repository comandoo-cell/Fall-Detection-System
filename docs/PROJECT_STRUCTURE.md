# Proje Yapısı Dokümantasyonu

## 📁 Tam Dizin Yapısı

```
all-detection-system/
│
├── .github/                          # GitHub ayarları
│   └── workflows/                    # CI/CD pipeline'ları
│       ├── tests.yml                 # Otomatik testler
│       └── code_quality.yml          # Kod kalitesi kontrolleri
│
├── src/                              # Kaynak kod
│   ├── core/                         # Çekirdek düşme tespit algoritmaları
│   │   ├── __init__.py
│   │   └── fall_detector.py          # Ana düşme tespit mantığı
│   │
│   ├── models/                       # ML model yönetimi
│   │   ├── __init__.py
│   │   ├── pose_estimator.py         # MediaPipe pose tespiti
│   │   └── multi_person_detector.py  # YOLOv8 çoklu kişi tespiti
│   │
│   ├── utils/                        # Yardımcı modüller
│   │   ├── __init__.py
│   │   ├── error_handler.py          # Hata işleme ve loglama
│   │   ├── video_processor.py        # Video işleme yardımcıları
│   │   └── video_url_handler.py      # URL video işleme
│   │
│   └── ui/                           # Kullanıcı arayüzü
│       ├── __init__.py
│       └── streamlit_app.py          # Streamlit web arayüzü
│
├── tests/                            # Birim testleri
│   ├── __init__.py
│   ├── test_fall_detector.py         # Düşme tespit testi
│   ├── test_pose_estimator.py        # Pose tespit testleri
│   └── test_integration.py           # Entegrasyon testleri
│
├── benchmarks/                       # Performans benchmark'ları
│   ├── run_benchmarks.py             # Benchmark çalıştırıcısı
│   ├── benchmark_results.json        # Sonuç çıktıları
│   └── README.md                     # Benchmark dokümantasyonu
│
├── examples/                         # Örnekler ve demolar
│   ├── README.md                     # Örnek dokümantasyonu
│   ├── RESULTS.md                    # Beklenen sonuçlar
│   ├── screenshots/                  # Arayüz ekran görüntüleri
│   ├── results/                      # Örnek test sonuçları
│   └── usage_examples/               # Kod örnekleri
│
├── docs/                             # Dokümantasyon
│   ├── API.md                        # API dokümantasyonu
│   ├── ARCHITECTURE.md               # Sistem mimarisi
│   ├── DEPLOYMENT.md                 # Dağıtım rehberi
│   └── FAQ.md                        # Sık sorulan sorular
│
├── configs/                          # Yapılandırma dosyaları
│   ├── default_config.yaml           # Varsayılan yapılandırma
│   └── production_config.yaml        # Production ayarları
│
├── logs/                             # Log dosyaları (git'e dahil değil)
│   └── fall_detection_YYYYMMDD.log   # Günlük log dosyaları
│
├── models/                           # Önceden eğitilmiş modeller
│   └── yolov8n-pose.pt               # YOLOv8 Nano Pose modeli
│
├── app_fast.py                       # Ana uygulama giriş noktası
├── requirements.txt                  # Python bağımlılıkları
├── .gitignore                        # Git ignore kuralları
├── LICENSE                           # MIT Lisansı
├── README.md                         # Ana dokümantasyon (Türkçe)
├── README_ACADEMIC.md                # Akademik dokümantasyon (Türkçe)
├── CONTRIBUTING.md                   # Katkı rehberi
└── CHANGELOG.md                      # Versiyon geçmişi
```

## 📦 Modül Organizasyonu

### Core Modülleri (`src/core/`)
**Amaç**: Çekirdek düşme tespit algoritmaları
- `fall_detector.py`: Ana düşme tespit mantığı
  - Çok kriterli analiz
  - Güven skoru hesaplama
  - Geçmiş takibi

### Modeller (`src/models/`)
**Amaç**: Makine öğrenimi model entegrasyonları
- `pose_estimator.py`: MediaPipe sarmalayıcısı
  - Tek kişi pose tespiti
  - 35+ FPS performans
  - 33 vücut landmark'ı

- `multi_person_detector.py`: YOLOv8 sarmalayıcısı
  - Çoklu kişi takibi
  - 20+ FPS performans
  - Bounding box tespiti

### Yardımcılar (`src/utils/`)
**Amaç**: Yardımcı fonksiyonlar ve araçlar
- `error_handler.py`: Merkezi hata işleme
  - Loglama sistemi
  - Hata kurtarma
  - Kullanıcı dostu mesajlar

- `video_processor.py`: Video işleme
  - Kare doğrulama
  - Kalite kontrolleri
  - Hata kurtarma

- `video_url_handler.py`: URL video desteği
  - YouTube/URL işleme
  - Akış yönetimi

### UI (`src/ui/`)
**Amaç**: Kullanıcı arayüzü bileşenleri
- `streamlit_app.py`: Web arayüzü
  - Gerçek zamanlı görüntüleme
  - Kontroller ve ayarlar
  - İstatistik paneli

## 🔧 Yapılandırma Yönetimi

### Yapılandırma Dosyaları
- `default_config.yaml`: Geliştirme ayarları
- `production_config.yaml`: Production ayarları

### Yapılandırma Yapısı
```yaml
detection:
  angle_threshold: 60.0
  confidence_threshold: 60.0
  velocity_threshold: 0.5

performance:
  max_fps: 30
  buffer_size: 1
  use_gpu: false

logging:
  level: INFO
  directory: logs/
  max_files: 30
```

## 🧪 Test Yapısı

### Birim Testleri (`tests/`)
- **test_fall_detector.py**: Çekirdek algoritma testleri
  - Açı hesaplama
  - En-boy oranı
  - Düşme tespit mantığı
  
- **test_pose_estimator.py**: Model entegrasyon testleri
  - MediaPipe fonksiyonelliği
  - YOLOv8 fonksiyonelliği
  - Hata işleme

### Benchmark'lar (`benchmarks/`)
- **run_benchmarks.py**: Performans benchmark'ı
  - Doğruluk metrikleri
  - Hız benchmark'ları
  - Kenar durum testleri

## 📊 Çıktı Yapısı

### Loglar (`logs/`)
```
logs/
└── fall_detection_20251217.log
```

### Sonuçlar (`examples/results/`)
```
results/
├── benchmark_results.json
├── confusion_matrix.png
└── performance_graph.png
```

## 🚀 Giriş Noktaları

### Ana Uygulama
```bash
streamlit run app_fast.py
```

### Testler
```bash
python -m pytest tests/ -v
```

### Benchmark'lar
```bash
python benchmarks/run_benchmarks.py
```

## 🔄 Veri Akışı

```
Kullanıcı Girdisi → Video Kaynağı
    ↓
Video Processor (doğrulama, hata işleme)
    ↓
Pose Tespiti (MediaPipe/YOLOv8)
    ↓
Düşme Dedektörü (çok kriterli analiz)
    ↓
UI Gösterimi + Loglama
```

## 📝 Dosya İsimlendirme Kuralları

- **Modüller**: `snake_case.py`
- **Sınıflar**: `PascalCase`
- **Fonksiyonlar**: `snake_case()`
- **Sabitler**: `UPPER_SNAKE_CASE`
- **Testler**: `test_*.py`
- **Configler**: `*_config.yaml`

## 🎯 En İyi Uygulamalar

1. **Modülerlik**: Her dosya tek bir sorumluluğa sahip olmalı
2. **Hata İşleme**: Kapsamlı try-except blokları
3. **Loglama**: Önemli tüm olaylar loglanmalı
4. **Testler**: Çekirdek fonksiyonlar için birim testleri
5. **Dokümantasyon**: Tüm public fonksiyonlar için docstring
6. **Type Hint'ler**: Mümkün olduğunca tip ipuçları kullanılmalı

## 🔐 Güvenlik

- Hassas veriler commit edilmiyor (`.gitignore`)
- Log dosyaları repository'ye dahil edilmiyor
- Yapılandırma dosyaları doğrulanıyor
- Giriş verileri sanitize ediliyor

## 📚 İlgili Dokümanlar

- [README.md](../README.md) - Ana dokümantasyon
- [README_ACADEMIC.md](../README_ACADEMIC.md) - Akademik detaylar
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Nasıl katkı yapılır
- [API.md](API.md) - API dokümantasyonu
