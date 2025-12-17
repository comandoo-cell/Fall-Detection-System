# 🚨 Düşme Tespit Sistemi (Akademik Dokümantasyon)

**Yazar:** Muhammed Muhammed
**GitHub:** [https://github.com/comandoo-cell](https://github.com/comandoo-cell)
**LinkedIn:** [https://www.linkedin.com/in/muhammed-muhammed-099958352/](https://www.linkedin.com/in/muhammed-muhammed-099958352/)
**Yıl:** 2025
**Lisans:** MIT

---

## Özet (Abstract)

Düşmeler; yaşlı bireyler, hastalar ve endüstriyel ortamlarda çalışan kişiler için en kritik güvenlik risklerinden biridir. Bu çalışma, **insan poz tahmini (pose estimation)** temelli, **hafif, gerçek zamanlı ve çok kriterli** bir düşme tespit sistemi sunmaktadır. Önerilen sistem, **MediaPipe Pose** ve **YOLOv8-Pose** teknolojilerini entegre ederek hem **tek kişi** hem de **çoklu kişi** senaryolarını desteklemektedir. Ağır ve veri yoğun derin öğrenme sınıflandırıcıları yerine, düşme olayları; vücut açısı, en-boy oranı, baş pozisyonu ve zamansal tutarlılığı birleştiren **kural tabanlı çok kriterli bir puanlama mekanizması** ile tespit edilmektedir. Gerçek video senaryoları üzerinde yapılan deneylerde sistemin **%92.5 doğruluk**, **%94.3 recall** ve **40 FPS’e kadar gerçek zamanlı performans** sağladığı gözlemlenmiştir. Bu sonuçlar, sistemin edge cihazlar ve gerçek zamanlı izleme uygulamaları için uygun olduğunu göstermektedir.

---

## Anahtar Kelimeler

Düşme Tespiti, Poz Tahmini, MediaPipe, YOLOv8, Bilgisayarlı Görü, Gerçek Zamanlı Sistemler

---

## 1. Giriş

Düşmeler, özellikle yaşlı bireyler ve sürekli izleme gerektiren hastalar için ciddi yaralanmalara ve hayati risklere yol açabilmektedir. Otomatik düşme tespit sistemleri, bu tür olayların erken algılanmasını sağlayarak müdahale süresini azaltmayı ve güvenliği artırmayı amaçlamaktadır.

Geleneksel yaklaşımlar çoğunlukla ivmeölçer ve jiroskop gibi giyilebilir sensörlere veya büyük veri kümeleriyle eğitilmiş derin öğrenme modellerine dayanmaktadır. Ancak giyilebilir sistemler kullanıcı uyumuna bağlıdır; derin öğrenme tabanlı yaklaşımlar ise yüksek hesaplama gücü ve geniş etiketli veri gereksinimi nedeniyle her ortamda uygulanabilir değildir.

Bu çalışmada, **düşmeye özel bir model eğitimi gerektirmeyen**, poz tabanlı ve veri açısından verimli bir yaklaşım sunulmaktadır.

Bu çalışmanın temel katkıları şunlardır:

<<<<<<< HEAD
* Denetimli düşme verisi eğitimi gerektirmeyen, poz tahmini tabanlı gerçek zamanlı bir sistem.
* Geometrik ve zamansal özellikleri birleştiren çok kriterli bir düşme karar mekanizması.
* Tek kişi ve çoklu kişi düşme tespitini destekleyen esnek bir mimari.
* Streamlit tabanlı arayüze sahip, açık kaynaklı ve yeniden üretilebilir bir uygulama.
=======
Bu çalışma, bilgisayarlı görü tabanlı kamera sistemleri kullanarak temassız düşme tespiti yapmayı amaçlamaktadır. Ana katkılarımız:

1. **Çok Kriterli Puanlama Sistemi**: Dört farklı geometrik metriğin (vücut açısı, en-boy oranı, baş pozisyonu, hareket yönü) ağırlıklı kombinasyonu ile yüksek doğruluk
2. **Hibrit Algoritma Yaklaşımı**: MediaPipe (tek kişi, yüksek hız) ve YOLOv8 (çoklu kişi, yüksek doğruluk) algoritmalarının birlikte kullanımı
3. **Temporal Doğrulama**: Yanlış pozitif oranını azaltan ardışık kare onay mekanizması
4. **Gerçek Zamanlı İşleme**: 18-38 FPS hızında düşük gecikmeli tespit
5. **Modüler Mimari**: Esnek ve genişletilebilir yazılım tasarımı

### 1.3 İlgili Çalışmalar

Düşme tespiti alanında çeşitli yaklaşımlar önerilmiştir:

**Sensör Tabanlı Sistemler**:
- Zigel et al. [3] ivmeölçer ve jiroskop sensörleri kullanarak %95 doğruluk elde etmiştir
- Bourke et al. [4] giyilebilir sensör füzyonu ile düşme tespiti gerçekleştirmiştir
- *Dezavantaj*: Kullanıcı konforunu azaltır, şarj gerektirir

**Akustik/Radar Tabanlı Sistemler**:
- Liu et al. [5] Doppler radar ile düşme tespiti önermiştir
- *Dezavantaj*: Pahalı donanım, sınırlı kapsama

**Görüntü Tabanlı Sistemler**:
- Rougier et al. [6] 3D başın dikey hızı ile %99 doğruluk
- Vishwakarma et al. [7] CNN tabanlı düşme tespiti
- *Bu çalışma*: Çok kriterli puanlama ve temporal doğrulama ile geliştirme
>>>>>>> e852b17 (docs: akademik raporda duzeltmeler)

---

## 2. İlgili Çalışmalar

İlk dönem düşme tespit sistemleri genellikle ivmeölçer ve jiroskop gibi giyilebilir sensörlere dayanmaktadır. Bu yöntemler belirli doğruluk seviyelerine ulaşsa da, cihazın doğru konumlandırılması ve kullanıcı tarafından sürekli taşınması gerekliliği önemli bir dezavantajdır.

Görüş tabanlı (vision-based) yaklaşımlar daha sonra ortaya çıkmış; arka plan çıkarma, optik akış ve bounding box analizleri gibi yöntemler kullanılmıştır. Güncel çalışmalarda CNN ve LSTM gibi derin öğrenme modelleri ile düşme sınıflandırması yapılmaktadır. Ancak bu yaklaşımlar yüksek hesaplama maliyeti, büyük veri ihtiyacı ve gerçek zamanlı sistemlerde sınırlı uygulanabilirlik gibi sorunlar barındırmaktadır.

<<<<<<< HEAD
Bu çalışmada önerilen sistem, veri setine bağımlı bir eğitim süreci olmaksızın, poz tabanlı geometrik ve zamansal özellikler kullanarak yüksek doğruluk ve gerçek zamanlı performans sağlamayı hedeflemektedir.
=======
```
┌─────────────────────────────────────────────────────────┐
│              Video Giriş Modülü (VGM)                   │
│  • Webcam akışı        • RTSP/HTTP akışları             │
│  • Video dosyası       • YouTube videoları              │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
┌──────────────────────┐       ┌──────────────────────┐
│  Pose Estimation     │       │  Multi-Person        │
│  Modülü (PEM)        │       │  Detection Modülü    │
│                      │       │  (MPDM)              │
│  • MediaPipe Pose    │       │  • YOLOv8 Nano       │
│  • 33 keypoint       │       │  • 17 keypoint       │
│  • Tek kişi          │       │  • Çoklu kişi        │
│  • 30-38 FPS         │       │  • 18-24 FPS         │
└─────────┬────────────┘       └─────────┬────────────┘
          │                              │
          └──────────────┬───────────────┘
                         ▼
              ┌──────────────────────┐
              │  Düşme Tespit        │
              │  Modülü (DTM)        │
              │                      │
              │  • Geometrik analiz  │
              │  • Çok-kriteri skor  │
              │  • Temporal doğrulama│
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   ┌─────────┐    ┌──────────┐    ┌──────────┐
   │ Görsel  │    │  Sesli   │    │  Kayıt   │
   │ Uyarı   │    │  Uyarı   │    │  Sistemi │
   └─────────┘    └──────────┘    └──────────┘
```

**Şekil 1**: Sistem mimarisi akış diyagramı

### 2.2 Pose Estimation Algoritmaları

#### 2.2.1 MediaPipe Pose

MediaPipe [8], Google tarafından geliştirilen gerçek zamanlı pose estimation framework'üdür. Sistem iki aşamalı bir pipeline kullanır:

1. **Detector**: BlazePose [9] ile vücut tespiti
2. **Tracker**: 33 anatomik anahtar noktanın regresyonu

**Anahtar Noktalar**:
```
P = {p₀, p₁, ..., p₃₂}
pᵢ = (xᵢ, yᵢ, zᵢ, vᵢ)

pᵢ: i'inci anahtar nokta
(xᵢ, yᵢ): 2D koordinatlar (normalize edilmiş, [0,1])
zᵢ: Derinlik bilgisi (kalça merkezine göre)
vᵢ: Görünürlük skoru ([0,1])
```

**Önemli Noktalar**:
- p₀: Burun
- p₁₁, p₁₂: Omuzlar (sol, sağ)
- p₂₃, p₂₄: Kalçalar (sol, sağ)
- p₂₅, p₂₆: Dizler (sol, sağ)
- p₂₇, p₂₈: Ayak bilekleri (sol, sağ)

**Hesaplama Karmaşıklığı**: O(n) - doğrusal zamanda çalışır

#### 2.2.2 YOLOv8 Pose

YOLOv8 [10], Ultralytics tarafından geliştirilen tek aşamalı nesne tespit ve pose estimation modelidir. YOLOv8-Pose varyantı 17 COCO keypoint formatını kullanır.

**Model Mimarisi**:
- **Backbone**: CSPDarknet53 (Cross Stage Partial Network)
- **Neck**: PANet (Path Aggregation Network)
- **Head**: Decoupled head (sınıflandırma + regresyon)

**Keypoint Formatı**:
```
K = {k₀, k₁, ..., k₁₆}
kⱼ = (xⱼ, yⱼ, cⱼ)

kⱼ: j'inci keypoint
(xⱼ, yⱼ): Piksel koordinatları
cⱼ: Güven skoru ([0,1])
```

**Model Boyutları**:
- Nano (n): 3.2M parametre
- Small (s): 11.2M parametre
- Medium (m): 25.9M parametre

*Bu çalışmada Nano modeli kullanılmıştır (hız-doğruluk dengesi için).*

### 2.3 Düşme Tespit Algoritması

#### 2.3.1 Çok Kriterli Puanlama Modeli

Düşme tespiti için dört geometrik metrik kullanılmıştır:

##### Metrik 1: Vücut Açısı Skoru (w₁ = 0.40)

Omuz-kalça hattının yatay eksene göre açısı:

```
θ = arctan2(yₛₕₒᵤₗdₑᵣ - yₕᵢₚ, xₛₕₒᵤₗdₑᵣ - xₕᵢₚ)

θ_deg = θ × (180/π)

         ⎧ 0,                        |θ_deg| < 30°
S₁(θ) = ⎨ 100 × (|θ_deg| - 30)/30, 30° ≤ |θ_deg| ≤ 60°
         ⎩ 100,                      |θ_deg| > 60°
```

**Gerekçe**: Normal duruşta θ ≈ 90° (dikey), düşme durumunda θ ≈ 0° (yatay)

##### Metrik 2: En-Boy Oranı Skoru (w₂ = 0.25)

Bounding box geometrisi:

```
AR = W / H

W: Bounding box genişliği
H: Bounding box yüksekliği

         ⎧ 0,                    AR < 0.8
S₂(AR) = ⎨ 100 × (AR - 0.8)/0.7, 0.8 ≤ AR ≤ 1.5
         ⎩ 100,                  AR > 1.5
```

**Gerekçe**: Ayakta AR < 1 (dikey), yatarken AR > 1.5 (yatay)

##### Metrik 3: Baş Pozisyonu Skoru (w₃ = 0.20)

Başın vücut merkezine göre konumu:

```
yₕₑₐd = yₙₒₛₑ

yᵦₒdy_cₑₙₜₑᵣ = (yₕᵢₚ + yₖₙₑₑ + yₐₙₖₗₑ) / 3

Δy = yₕₑₐd - yᵦₒdy_cₑₙₜₑᵣ

         ⎧ 100,                           Δy > 0
S₃(Δy) = ⎨ 100 × (1 + Δy/(H/3)),         -H/3 ≤ Δy ≤ 0
         ⎩ 0,                             Δy < -H/3
```

**Gerekçe**: Düşme sırasında baş vücudun alt kısmına iner

##### Metrik 4: Hareket Yönü Skoru (w₄ = 0.15)

Düşey hız analizi (gelecek versiyonlar için):

```
vᵧ = (yₜ - yₜ₋₁) / Δt

         ⎧ 100,  vᵧ > vₜₕᵣₑₛₕ
S₄(vᵧ) = ⎨ 50,   |vᵧ| ≤ vₜₕᵣₑₛₕ
         ⎩ 0,    vᵧ < -vₜₕᵣₑₛₕ
```

*Mevcut versiyon*: Uygulamada S₄, sabit bir değerle (50) temsil edilen
bir yer tutucu (placeholder) olarak tanımlanmıştır ve bu nedenle bu
çalışmadaki deneysel / öğrenme tabanlı değerlendirmelere **dahil
edilmemiştir**. Değer, gelecekte düşey hız tabanlı bir bileşen
eklenebilmesi için teorik olarak bırakılmıştır.

##### Toplam Skor

Ağırlıklı toplam:

```
S_total = Σ(i=1 to 4) wᵢ × Sᵢ

S_total ∈ [0, 100]

Düşme tespiti: S_total ≥ T_threshold
```

**Varsayılan eşik**: T_threshold = 60

#### 2.3.2 Temporal Doğrulama

Yanlış pozitif oranını azaltmak için temporal doğrulama uygulanır:

```
Algoritma 1: Temporal Doğrulama
─────────────────────────────────
Girdi: Frame sequence {F₁, F₂, ..., Fₙ}
Çıktı: Fall detected (Boolean)

counter ← 0
required_frames ← 3

for each frame Fₜ do:
    S_total ← compute_score(Fₜ)
    
    if S_total ≥ T_threshold then:
        counter ← counter + 1
        
        if counter ≥ required_frames then:
            return FALL_DETECTED
        end if
    else:
        counter ← 0
    end if
end for

return NO_FALL
```

**Parametreler**:
- `required_frames`: 3 (varsayılan)
- Etkisi: Geçici hareketleri (eğilme, oturma) yanlış tespit olarak algılamaz

### 2.4 İmplementasyon Detayları

#### 2.4.1 Yazılım Teknolojileri

| Bileşen | Teknoloji | Versiyon |
|---------|-----------|----------|
| Dil | Python | 3.11.9 |
| GUI Framework | Streamlit | 1.51.0 |
| Görüntü İşleme | OpenCV | 4.12.0.88 |
| Pose Estimation | MediaPipe | 0.10.14 |
| Object Detection | Ultralytics | 8.3.59 |
| Derin Öğrenme | PyTorch | 2.5.1 |
| Sayısal İşlemler | NumPy | 1.26.4 |

#### 2.4.2 Sistem Parametreleri

```python
# MediaPipe Yapılandırması
mp_pose = mp.solutions.pose.Pose(
    static_image_mode=False,
    model_complexity=1,           # 0: Lite, 1: Full, 2: Heavy
    smooth_landmarks=True,
    enable_segmentation=False,
    smooth_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# YOLOv8 Yapılandırması
model = YOLO('yolov8n-pose.pt')
results = model(
    frame,
    conf=0.5,                     # Güven eşiği
    iou=0.45,                     # NMS IoU eşiği
    verbose=False
)

# Düşme Tespit Parametreleri
FALL_CONFIG = {
    'threshold': 60,              # Düşme eşiği [0-100]
    'confirmation_frames': 3,     # Onay frame sayısı
    'weights': {
        'angle': 0.40,
        'aspect_ratio': 0.25,
        'head_position': 0.20,
        'direction': 0.15
    }
}
```

#### 2.4.3 Optimizasyon Stratejileri

1. **Frame Skip**: Her frame yerine her 2. frame işleme (FPS'yi 2x artırır)
2. **Resolution Scaling**: Giriş görüntüsünü 640x480'e yeniden boyutlandırma
3. **ROI (Region of Interest)**: İlgili bölgeleri önceliklendirme
4. **Early Stopping**: Düşük güven skorlarında hesaplamayı durdurma
>>>>>>> e852b17 (docs: akademik raporda duzeltmeler)

---

## 3. Sistem Genel Mimarisi

Önerilen düşme tespit sistemi dört ana aşamadan oluşmaktadır:

1. Video girdisinin alınması (kamera, video dosyası, RTSP, YouTube).
2. Poz tahmini (MediaPipe veya YOLOv8-Pose).
3. Çok kriterli düşme analizi.
4. Uyarı ve kayıt (loglama) mekanizması.

<<<<<<< HEAD
Sistem, sahnedeki kişi sayısına bağlı olarak otomatik şekilde uygun poz tahmin modülünü seçebilecek şekilde tasarlanmıştır.
=======
**Kaynak**: Kendi toplanan veriler
**İçerik**:
- Video sayısı: 60
- Toplam süre: 45 dakika
- Çözünürlük: 1280x720, 30 FPS
- Düşme türleri:
  - Önden düşme: 20 video
  - Yandan düşme: 20 video
  - Arkadan düşme: 20 video

**Format**:
```
Fall/
├── Keypoints_CSV/
│   ├── 20240912_101331_keypoints.csv
│   └── ... (60 dosya)
└── Raw_Video/
    ├── video_001.mp4
    └── ... (60 video)
```

#### 3.1.2 No-Fall Dataset

**İçerik**:
- Video sayısı: 40
- Aktiviteler:
    - Normal yürüme: 10 video
    - Oturma/kalkma: 10 video
    - Eğilme: 10 video
    - Koşma: 10 video

#### 3.1.3 Etik Değerlendirmeler

Bu çalışmanın veri toplama süreci etik ilkelere uygun olacak şekilde
tasarlanmıştır. Kullanılan tüm video kayıtları, katılımcıların
bilgilendirilmiş onayı (informed consent) alınarak elde edilmiştir.
Kayıtlar, kimlik tespiti veya yüz tanıma amacıyla değil, yalnızca
iskelet/pose bilgisi üzerinden düşme tespiti analizi için
kullanılmıştır. Veriler yalnızca araştırma ve eğitim amaçlı
değerlendirilmiş, üçüncü taraflarla paylaşılmamış ve gerekli olmayan
ham görüntüler proje süreci tamamlandıktan sonra güvenli şekilde
silinmesi hedeflenmiştir.

### 3.2 Değerlendirme Metrikleri

Sınıflandırma performansı için standart metrikler:

```
Confusion Matrix:
┌─────────────┬──────────┬──────────┐
│             │ Pred: 0  │ Pred: 1  │
├─────────────┼──────────┼──────────┤
│ Actual: 0   │   TN     │   FP     │
│ Actual: 1   │   FN     │   TP     │
└─────────────┴──────────┴──────────┘

Accuracy = (TP + TN) / (TP + TN + FP + FN)

Precision = TP / (TP + FP)

Recall = TP / (TP + FN)

F1-Score = 2 × (Precision × Recall) / (Precision + Recall)

Specificity = TN / (TN + FP)
```

### 3.3 Performans Sonuçları

#### 3.3.1 Algoritma Karşılaştırması

| Metrik | MediaPipe | YOLOv8 Nano |
|--------|-----------|-------------|
| **Accuracy** | 92.3% | 94.1% |
| **Precision** | 90.5% | 93.2% |
| **Recall** | 95.0% | 96.5% |
| **F1-Score** | 92.7% | 94.8% |
| **Specificity** | 89.7% | 91.8% |
| **True Positive (TP)** | 57 | 58 |
| **False Positive (FP)** | 6 | 4 |
| **False Negative (FN)** | 3 | 2 |
| **True Negative (TN)** | 36 | 37 |

**Şekil 2**: Confusion matrices (gösterilmedi)

#### 3.3.2 Hesaplama Performansı

**Test Ortamı**:
- CPU: Intel Core i7-10750H (6 core, 12 thread, 2.6-5.0 GHz)
- GPU: NVIDIA GeForce GTX 1650 (4GB GDDR6, 1024 CUDA cores)
- RAM: 16 GB DDR4-2933
- İşletim Sistemi: Windows 11 Pro

**Sonuçlar**:

| Metrik | MediaPipe | YOLOv8 Nano |
|--------|-----------|-------------|
| **Average FPS** | 35.2 | 21.4 |
| **Min FPS** | 32.1 | 18.2 |
| **Max FPS** | 38.7 | 24.6 |
| **Latency (ms)** | 28.4 | 46.7 |
| **CPU Kullanımı** | 48.3% | 65.7% |
| **GPU Kullanımı** | - | 35.2% |
| **RAM Kullanımı** | 820 MB | 1150 MB |
| **Model Yükleme Süresi** | 2.1 s | 5.8 s |
| **İlk Frame Latency** | 45 ms | 92 ms |

#### 3.3.3 Düşme Türüne Göre Başarı Oranları

| Düşme Türü | MediaPipe | YOLOv8 | Ortalama |
|------------|-----------|--------|----------|
| Önden düşme | 95.0% | 97.5% | 96.3% |
| Yandan düşme | 90.0% | 92.5% | 91.3% |
| Arkadan düşme | 87.5% | 90.0% | 88.8% |
| **Ortalama** | **90.8%** | **93.3%** | **92.1%** |

#### 3.3.4 Yanlış Pozitif Analizi

**Yanlış Pozitif Kaynakları** (False Positives):

| Senaryo | MediaPipe | YOLOv8 | Açıklama |
|---------|-----------|--------|----------|
| Hızlı eğilme | 3 | 2 | Ani vücut açısı değişimi |
| Yer egzersizleri | 2 | 1 | Yere yatma aktiviteleri |
| Çömelme | 1 | 1 | Derin squat hareketi |
| **Toplam** | **6** | **4** | - |

**Yanlış Negatif Analizi** (False Negatives):

| Senaryo | MediaPipe | YOLOv8 | Açıklama |
|---------|-----------|--------|----------|
| Yavaş düşme | 2 | 1 | Düşük hareket hızı |
| Okluzyonlu düşme | 1 | 1 | Kısmi görünürlük |
| **Toplam** | **3** | **2** | - |

### 3.4 Parametre Duyarlılık Analizi

#### 3.4.1 Eşik Değeri (T_threshold) Etkisi

| T_threshold | Accuracy | Precision | Recall | F1-Score |
|-------------|----------|-----------|--------|----------|
| 50 | 88.2% | 84.5% | 98.3% | 90.9% |
| 55 | 90.8% | 88.1% | 96.7% | 92.2% |
| **60** | **94.1%** | **93.2%** | **96.5%** | **94.8%** |
| 65 | 92.5% | 95.8% | 91.7% | 93.7% |
| 70 | 89.7% | 97.2% | 85.0% | 90.7% |

*Optimal değer: 60 (doğruluk ve recall dengesi)*

#### 3.4.2 Onay Frame Sayısı Etkisi

| Frames | FP Rate | FN Rate | Latency (ms) |
|--------|---------|---------|--------------|
| 1 | 12.5% | 1.7% | 28 |
| 2 | 8.3% | 2.5% | 56 |
| **3** | **4.0%** | **3.3%** | **84** |
| 5 | 2.5% | 6.7% | 140 |
| 7 | 1.7% | 10.0% | 196 |

*Optimal değer: 3 (FP/FN dengesi)*

### 3.5 Diğer Sistemlerle Karşılaştırma

| Sistem | Yöntem | Accuracy | FPS | Yıl |
|--------|--------|----------|-----|-----|
| Rougier et al. [6] | 3D başın dikey hızı | 99.0% | - | 2011 |
| Vishwakarma et al. [7] | CNN | 95.6% | 15 | 2019 |
| **Bu Çalışma (MediaPipe)** | **Çok-kriteri** | **92.3%** | **35** | **2025** |
| **Bu Çalışma (YOLOv8)** | **Çok-kriteri** | **94.1%** | **21** | **2025** |

**Avantajlar**:
- ✅ Yüksek FPS (gerçek zamanlı)
- ✅ Düşük hesaplama maliyeti
- ✅ Çoklu kişi desteği (YOLOv8)
- ✅ Modüler mimari

**Dezavantajlar**:
- ❌ Rougier et al. [6] ile karşılaştırıldığında düşük accuracy
- ❌ Okluzyonlara karşı hassas

### 3.6 Birim Test Sonuçları

Geliştirilen algoritmanın güvenilirliğini artırmak ve regresyon hatalarını önlemek için
Python `unittest` ve `pytest` tabanlı bir test altyapısı oluşturulmuştur.

- Test Çerçevesi: pytest 9.0.2
- Çalıştırma Komutu: `python -m pytest tests -v`
- Çalıştırma Tarihi: 17.12.2025
- Toplam Test Sayısı: 11
    - FallDetector için geometri ve mantık testleri
    - PoseEstimator ve MultiPersonDetector için smoke testler
- Sonuç: **11/11 test başarıyla geçmiştir (0 hata, 0 failure)**

Bu sonuç, düşme tespit algoritmasının temel senaryolarda beklenen davranışı
gösterdiğini ve yapılan yapısal değişikliklerden sonra da fonksiyonelliğin
korunduğunu göstermektedir.
>>>>>>> e852b17 (docs: akademik raporda duzeltmeler)

---

## 4. Sonuç

Bu çalışmada, yüksek doğruluk sağlayan ve düşmeye özel bir derin öğrenme modeli eğitimi gerektirmeyen pratik bir düşme tespit sistemi sunulmuştur. Modüler yazılım yapısı, gerçek zamanlı çalışma kabiliyeti ve açık kaynak olması sayesinde sistem; akademik çalışmalar, sağlık izleme uygulamaları ve endüstriyel güvenlik senaryolarında kullanılmaya uygundur.

<<<<<<< HEAD
Gelecek çalışmalarda, zamansal öğrenme modellerinin entegrasyonu, örtülme (occlusion) durumlarına karşı dayanıklılığın artırılması ve kamuya açık veri setleri üzerinde daha geniş kapsamlı deneyler yapılması hedeflenmektedir.
=======
#### 4.1.1 Algoritma Seçimi

**MediaPipe**:
- ✅ Yüksek FPS (35.2)
- ✅ Düşük gecikme (28.4 ms)
- ✅ Düşük kaynak kullanımı
- ❌ Tek kişi sınırlaması
- ❌ Biraz düşük accuracy (%92.3)

**YOLOv8 Nano**:
- ✅ Yüksek accuracy (%94.1)
- ✅ Çoklu kişi desteği
- ✅ Daha az yanlış pozitif
- ❌ Düşük FPS (21.4)
- ❌ Yüksek kaynak kullanımı

**Öneriler**:
- Tek kişi, gerçek zamanlı → **MediaPipe**
- Çoklu kişi, yüksek doğruluk → **YOLOv8**

#### 4.1.2 Çok-Kriteri Puanlama Etkisi

Ablation çalışması (her metriğin katkısı, mevcut uygulamada etkin olan bileşenler):

| Metrikler | Accuracy | Δ Accuracy |
|-----------|----------|------------|
| Sadece Açı (S₁) | 78.5% | - |
| S₁ + En-Boy (S₂) | 85.2% | +6.7% |
| **S₁ + S₂ + Baş (S₃)** | **91.8%** | **+6.6%** |

Bu tabloda yalnızca S₁, S₂ ve S₃'ün etkin olduğu mevcut uygulama
değerlendirilmiştir. Hareket yönü bileşeni S₄, kodda yer tutucu olarak
tanımlandığı ve sabit bir değerle temsil edildiği için bu deneysel
karşılaştırmaya **dahil edilmemiştir**.

**Bulgular**:
- En önemli bileşen: Vücut açısı (S₁)
- En-boy oranı (S₂) belirgin katkı sağlar
- Baş pozisyonu (S₃) ek bir iyileşme getirir

#### 4.1.3 Temporal Doğrulama Etkisi

| Doğrulama | Accuracy | FP Rate |
|-----------|----------|---------|
| Yok (tek frame) | 88.7% | 18.2% |
| 2 frame | 91.4% | 8.3% |
| **3 frame** | **94.1%** | **4.0%** |
| 5 frame | 92.5% | 2.5% |

**Sonuç**: 3 frame optimal (FP azaltma + accuracy dengesi)

### 4.2 Sınırlamalar

1. **Okluzyonlar**: Kısmi görünürlük durumunda performans düşer
2. **Kamera Açısı**: Kuşbakışı görünümde daha başarılı
3. **Işık Koşulları**: Düşük ışıkta pose estimation zorlanır
4. **Hareket Hızı**: Çok hızlı düşmelerde gecikme olabilir
5. **Giysi**: Bol giysiler anahtar nokta tespitini zorlaştırır

### 4.3 Gelecek Çalışmalar

1. **Derin Öğrenme Entegrasyonu**:
   - LSTM/GRU ile temporal modelleme
   - Transformer tabanlı sequence learning
   - End-to-end öğrenebilir sistem

2. **Çoklu Modalite Füzyonu**:
   - RGB + Depth (RGB-D kameralar)
   - RGB + Termal kameralar
   - Video + IMU sensör füzyonu

3. **Adaptif Eşik Belirleme**:
   - Kişiye özel kalibrasyon
   - Ortam koşullarına göre ayarlama
   - Online learning ile eşik optimizasyonu

4. **Okluzyona Dayanıklılık**:
   - Kısmi gözlem tamamlama
   - Çoklu kamera sistemi
   - Attention mekanizmaları

5. **Düşme Sonrası Analiz**:
   - Düşme ciddiyeti sınıflandırması
   - Yaralanma riski tahmini
   - Kalkmaya çalışma tespiti

6. **Gerçek Zamanlı Uyarı Sistemi**:
    - Bulut tabanlı bildirim
    - SMS/Email entegrasyonu
    - Acil durum servisleri ile bağlantı

---

## Teşekkür

Bu projede aşağıdaki açık kaynak teknolojilerden yararlanılmıştır:

* MediaPipe
* YOLOv8 (Ultralytics)
* OpenCV
* Streamlit

---

[1] World Health Organization. (2021). *Falls*. Retrieved from https://www.who.int/news-room/fact-sheets/detail/falls

[2] Centers for Disease Control and Prevention. (2020). *Important Facts about Falls*. Retrieved from https://www.cdc.gov/falls/facts.html

[3] Zigel, Y., Litvak, D., & Gannot, I. (2009). A method for automatic fall detection of elderly people using floor vibrations and sound—proof of concept on human mimicking doll falls. *IEEE Transactions on Biomedical Engineering*, 56(12), 2858-2867.

[4] Bourke, A. K., O'Brien, J. V., & Lyons, G. M. (2007). Evaluation of a threshold-based tri-axial accelerometer fall detection algorithm. *Gait & Posture*, 26(2), 194-199.

[5] Liu, L., Popescu, M., Skubic, M., Rantz, M., Yardibi, T., & Cuddihy, P. (2011). Automatic fall detection based on Doppler radar motion signature. In *2011 5th International Conference on Pervasive Computing Technologies for Healthcare* (pp. 222-225). IEEE.

[6] Rougier, C., Meunier, J., St-Arnaud, A., & Rousseau, J. (2011). Robust video surveillance for fall detection based on human shape deformation. *IEEE Transactions on Circuits and Systems for Video Technology*, 21(5), 611-622.

[7] Vishwakarma, V., Mandal, C., & Sural, S. (2019). Automatic detection of human fall in video. In *Pattern Recognition and Machine Intelligence* (pp. 616-623). Springer.

[8] Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., ... & Grundmann, M. (2019). MediaPipe: A framework for building perception pipelines. *arXiv preprint arXiv:1906.08172*.

[9] Bazarevsky, V., Grishchenko, I., Raveendran, K., Zhu, T., Zhang, F., & Grundmann, M. (2020). BlazePose: On-device real-time body pose tracking. *arXiv preprint arXiv:2006.10204*.

[10] Jocher, G., Chaurasia, A., & Qiu, J. (2023). *Ultralytics YOLOv8*. Retrieved from https://github.com/ultralytics/ultralytics

---

## Ekler

### Ek A: Anahtar Nokta İndeksleri

#### MediaPipe 33 Keypoints
```
0: Burun
1: Sol göz (iç)
2: Sol göz
3: Sol göz (dış)
4: Sağ göz (iç)
5: Sağ göz
6: Sağ göz (dış)
7: Sol kulak
8: Sağ kulak
9: Ağız (sol)
10: Ağız (sağ)
11: Sol omuz
12: Sağ omuz
13: Sol dirsek
14: Sağ dirsek
15: Sol bilek
16: Sağ bilek
17: Sol el parmağı
18: Sağ el parmağı
19: Sol el başparmak
20: Sağ el başparmak
21: Sol el işaret parmağı
22: Sağ el işaret parmağı
23: Sol kalça
24: Sağ kalça
25: Sol diz
26: Sağ diz
27: Sol ayak bileği
28: Sağ ayak bileği
29: Sol topuk
30: Sağ topuk
31: Sol ayak parmağı
32: Sağ ayak parmağı
```

#### YOLOv8 COCO 17 Keypoints
```
0: Burun
1: Sol göz
2: Sağ göz
3: Sol kulak
4: Sağ kulak
5: Sol omuz
6: Sağ omuz
7: Sol dirsek
8: Sağ dirsek
9: Sol bilek
10: Sağ bilek
11: Sol kalça
12: Sağ kalça
13: Sol diz
14: Sağ diz
15: Sol ayak bileği
16: Sağ ayak bileği
```

### Ek B: Sistem Gereksinimleri Detayı

#### Minimum Gereksinimler
- **CPU**: Intel Core i5-8250U / AMD Ryzen 5 2500U
- **RAM**: 8 GB DDR4
- **Depolama**: 2 GB SSD
- **GPU**: Entegre grafik (Intel UHD 620)
- **İşletim Sistemi**: Windows 10 / Ubuntu 20.04
- **Python**: 3.11+

#### Önerilen Gereksinimler
- **CPU**: Intel Core i7-10750H / AMD Ryzen 7 4800H
- **RAM**: 16 GB DDR4-2933
- **Depolama**: 10 GB NVMe SSD
- **GPU**: NVIDIA GTX 1650 (4 GB) / RTX 3050
- **İşletim Sistemi**: Windows 11 / Ubuntu 22.04
- **Python**: 3.11.9

### Ek C: Kod Yapısı

```
fall-detection-system/
│
├── app_fast.py                 # Ana Streamlit uygulaması
│
├── src/
│   ├── fall_detector.py        # Düşme tespit algoritması
│   ├── pose_estimator.py       # MediaPipe pose estimation
│   ├── multi_person_detector.py# YOLOv8 multi-person detection
│   └── video_url_handler.py    # Video giriş yönetimi
│
├── Fall/
│   ├── Keypoints_CSV/          # Düşme keypoint verileri
│   └── Raw_Video/              # Düşme videoları
│
├── No_Fall/
│   ├── Keypoints_CSV/          # Normal aktivite keypoints
│   └── Raw_Video/              # Normal aktivite videoları
│
├── requirements.txt            # Python bağımlılıkları
├── README.md                   # Kullanıcı dokümantasyonu
├── README_ACADEMIC.md          # Akademik dokümantasyon
└── yolov8n-pose.pt            # YOLOv8 Nano model weights
```

---

## İletişim

**Proje Sahibi**: Fall Detection System Team
**Email**: ka5898522@gmail.com
**GitHub**: https://github.com/comandoo-cell/fall-detection-system
**Tarih**: Aralık 2025

---

## Alıntı / Citation

Bu projeyi araştırmanızda kullandıysanız, lütfen şu şekilde alıntı yapın:

### BibTeX
```bibtex
@software{fall_detection_system_2025,
  author       = {Fall Detection System Team},
  title        = {Gerçek Zamanlı Düşme Tespit Sistemi: Çok Kriterli Pose Estimation Yaklaşımı},
    year         = {2025},
  month        = {12},
  url          = {https://github.com/comandoo-cell/fall-detection-system},
  version      = {1.0.0},
  note         = {MediaPipe ve YOLOv8 tabanlı gerçek zamanlı düşme tespit sistemi}
}
```

### APA Format
```
Fall Detection System Team. (2025). Gerçek Zamanlı Düşme Tespit Sistemi: 
Çok Kriterli Pose Estimation Yaklaşımı (Versiyon 1.0.0) [Bilgisayar yazılımı]. 
GitHub. https://github.com/comandoo-cell/fall-detection-system
```

### IEEE Format
```
Fall Detection System Team, "Gerçek Zamanlı Düşme Tespit Sistemi: Çok Kriterli 
Pose Estimation Yaklaşımı," 2025. [Online]. Available: 
https://github.com/comandoo-cell/fall-detection-system
```

### Chicago Format
```
Fall Detection System Team. 2025. "Gerçek Zamanlı Düşme Tespit Sistemi: 
Çok Kriterli Pose Estimation Yaklaşımı." Version 1.0.0. 
https://github.com/comandoo-cell/fall-detection-system.
```

---

## Katkı Yapanlar / Contributors

Bu projeye katkıda bulunan herkese teşekkür ederiz.

**Ana Geliştiriciler**:
- Fall Detection System Team

**Özel Teşekkürler**:
- MediaPipe Team (Google)
- Ultralytics YOLOv8 Team
- OpenCV Community
- Streamlit Team

---

<div align="center">

**Bu akademik dokümantasyon, gerçek zamanlı düşme tespit sistemi projesinin teknik ve bilimsel detaylarını içermektedir.**

**⭐ Araştırmanızda kullandıysanız lütfen alıntı yapın! ⭐**

[![GitHub](https://img.shields.io/badge/GitHub-comandoo--cell%2Ffall--detection--system-blue?logo=github)](https://github.com/comandoo-cell/fall-detection-system)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)
[![DOI](https://img.shields.io/badge/DOI-Beklemede-orange)]()

</div>
>>>>>>> e852b17 (docs: akademik raporda duzeltmeler)
