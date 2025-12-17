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

* Denetimli düşme verisi eğitimi gerektirmeyen, poz tahmini tabanlı gerçek zamanlı bir sistem.
* Geometrik ve zamansal özellikleri birleştiren çok kriterli bir düşme karar mekanizması.
* Tek kişi ve çoklu kişi düşme tespitini destekleyen esnek bir mimari.
* Streamlit tabanlı arayüze sahip, açık kaynaklı ve yeniden üretilebilir bir uygulama.

---

## 2. İlgili Çalışmalar

İlk dönem düşme tespit sistemleri genellikle ivmeölçer ve jiroskop gibi giyilebilir sensörlere dayanmaktadır. Bu yöntemler belirli doğruluk seviyelerine ulaşsa da, cihazın doğru konumlandırılması ve kullanıcı tarafından sürekli taşınması gerekliliği önemli bir dezavantajdır.

Görüş tabanlı (vision-based) yaklaşımlar daha sonra ortaya çıkmış; arka plan çıkarma, optik akış ve bounding box analizleri gibi yöntemler kullanılmıştır. Güncel çalışmalarda CNN ve LSTM gibi derin öğrenme modelleri ile düşme sınıflandırması yapılmaktadır. Ancak bu yaklaşımlar yüksek hesaplama maliyeti, büyük veri ihtiyacı ve gerçek zamanlı sistemlerde sınırlı uygulanabilirlik gibi sorunlar barındırmaktadır.

Bu çalışmada önerilen sistem, veri setine bağımlı bir eğitim süreci olmaksızın, poz tabanlı geometrik ve zamansal özellikler kullanarak yüksek doğruluk ve gerçek zamanlı performans sağlamayı hedeflemektedir.

---

## 3. Sistem Genel Mimarisi

Önerilen düşme tespit sistemi dört ana aşamadan oluşmaktadır:

1. Video girdisinin alınması (kamera, video dosyası, RTSP, YouTube).
2. Poz tahmini (MediaPipe veya YOLOv8-Pose).
3. Çok kriterli düşme analizi.
4. Uyarı ve kayıt (loglama) mekanizması.

Sistem, sahnedeki kişi sayısına bağlı olarak otomatik şekilde uygun poz tahmin modülünü seçebilecek şekilde tasarlanmıştır.

---

## 4. Sonuç

Bu çalışmada, yüksek doğruluk sağlayan ve düşmeye özel bir derin öğrenme modeli eğitimi gerektirmeyen pratik bir düşme tespit sistemi sunulmuştur. Modüler yazılım yapısı, gerçek zamanlı çalışma kabiliyeti ve açık kaynak olması sayesinde sistem; akademik çalışmalar, sağlık izleme uygulamaları ve endüstriyel güvenlik senaryolarında kullanılmaya uygundur.

Gelecek çalışmalarda, zamansal öğrenme modellerinin entegrasyonu, örtülme (occlusion) durumlarına karşı dayanıklılığın artırılması ve kamuya açık veri setleri üzerinde daha geniş kapsamlı deneyler yapılması hedeflenmektedir.

---

## Teşekkür

Bu projede aşağıdaki açık kaynak teknolojilerden yararlanılmıştır:

* MediaPipe
* YOLOv8 (Ultralytics)
* OpenCV
* Streamlit

---


