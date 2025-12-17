# Projeyi GitHub'a Yükleme Rehberi / GitHub Upload Guide

Bu belge, projenizi GitHub'a nasıl yükleyeceğinizi adım adım açıklar.

## ✅ Yükleme Öncesi Kontrol Listesi

- [x] LICENSE dosyası eklendi
- [x] .gitignore yapılandırıldı
- [x] README.md hazırlandı (Türkçe)
- [x] README_ACADEMIC.md hazırlandı (akademik versiyon)
- [x] CHANGELOG.md oluşturuldu
- [x] requirements.txt güncellendi
- [x] Tüm kodlar temiz ve yorumlanmış

## 🚀 Adım 1: GitHub Repository Oluşturma

1. GitHub.com'a giriş yapın
2. Sağ üst köşeden "+" → "New repository" seçin
3. Repository bilgileri:
   - **İsim**: `fall-detection-system`
   - **Açıklama**: "Gerçek zamanlı düşme tespit sistemi - MediaPipe & YOLOv8"
   - **Görünürlük**: Public (herkese açık) veya Private (özel)
   - **README.md ekleme**: HAYIR (zaten var)
   - **LICENSE ekleme**: HAYIR (zaten var)
4. "Create repository" butonuna tıklayın

## 🔧 Adım 2: Git Kurulumu (İlk kez kullanıyorsanız)

### Windows için:
```powershell
# Git'in kurulu olup olmadığını kontrol edin
git --version

# Kurulu değilse: https://git-scm.com/download/win adresinden indirin
```

### Git Yapılandırması:
```powershell
git config --global user.name "Kullanıcı Adınız"
git config --global user.email "email@example.com"
```

## 📤 Adım 3: Projeyi GitHub'a Yükleme

### PowerShell'de projenizin klasöründe:

```powershell
# 1. Git repository'sini başlatın
cd "C:\Users\MSI GAMING\Desktop\my project"
git init

# 2. Tüm dosyaları staging area'ya ekleyin
git add .

# 3. İlk commit'i oluşturun
git commit -m "İlk commit: Düşme tespit sistemi v1.0.0"

# 4. Ana branch'i oluşturun (main)
git branch -M main

# 5. GitHub repository'sini bağlayın
# Not: 'comandoo-cell' yerine kendi kullanıcı adınızı yazın
git remote add origin https://github.com/comandoo-cell/fall-detection-system.git

# 6. Projeyi GitHub'a yükleyin
git push -u origin main
```

## 🔐 GitHub Authentication

### Personal Access Token (Önerilen)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → "Generate new token (classic)"
3. Yetkileri seçin:
   - ✅ repo (tüm yetkiler)
   - ✅ workflow
4. Token'ı kopyalayın (bir daha gösterilmez!)
5. Push yaparken:
   - Username: GitHub kullanıcı adınız
   - Password: Token'ınız (şifre değil!)

### SSH (Alternatif)

```powershell
# SSH key oluştur
ssh-keygen -t ed25519 -C "email@example.com"

# Public key'i kopyala
Get-Content ~/.ssh/id_ed25519.pub | clip

# GitHub → Settings → SSH and GPG keys → New SSH key
# Kopyalanan key'i yapıştırın

# SSH ile remote bağlantı
git remote set-url origin git@github.com:comandoo-cell/fall-detection-system.git
```

## 📋 Adım 4: GitHub Repository Düzenleme

### README.md'yi ana sayfa yap
- GitHub repository'nizde README.md otomatik görünecek

### About Bölümünü Düzenle
1. Repository sayfasında sağ üstten "⚙️ Settings" (değil, "About" yanındaki küçük dişli)
2. Bilgileri girin:
   - **Description**: "Gerçek zamanlı düşme tespit sistemi - MediaPipe & YOLOv8 pose estimation ile %94 doğruluk"
   - **Website**: (Varsa Streamlit Cloud linki)
   - **Topics**: `fall-detection`, `computer-vision`, `mediapipe`, `yolov8`, `pose-estimation`, `streamlit`, `opencv`, `python`, `real-time`, `healthcare`

### GitHub Pages (Opsiyonel)
1. Settings → Pages
2. Source: Deploy from branch → main → /docs
3. Dokümantasyon sitesi oluşturabilirsiniz

## 🏷️ Adım 5: İlk Release Oluşturma

```powershell
# Tag oluştur
git tag -a v1.0.0 -m "Release v1.0.0: İlk kararlı sürüm"
git push origin v1.0.0
```

### GitHub'da Release:
1. Repository → Releases → "Create a new release"
2. Tag: v1.0.0
3. Title: "v1.0.0 - İlk Kararlı Sürüm"
4. Açıklama: CHANGELOG.md'den kopyalayın
5. "Publish release"

## 📦 Adım 6: Gelecek Güncellemeler

```powershell
# Değişiklikleri ekle
git add .

# Commit yap
git commit -m "Açıklama mesajı"

# GitHub'a gönder
git push origin main
```

## 🎨 Bonus: Repository Görselleştirme

### Badges Ekleme
README.md'nizde zaten var:
- Python version
- Streamlit version
- License
- vb.

### Social Preview Image
1. Repository → Settings → Options → Social preview
2. Bir kapak görseli yükleyin (1280x640 px önerilen)

### GitHub Actions (CI/CD)
`.github/workflows/python-app.yml` oluşturarak otomatik testler ekleyebilirsiniz

## ❓ Sık Sorulan Sorular

### Q: .venv klasörü yüklenmesin
A: `.gitignore` dosyasında zaten var, yüklenmeyecek

### Q: fall_screenshots klasörü yüklensin mi?
A: `.gitignore`'da yok, yüklenecek. İstemiyorsanız ekleyin:
```
fall_screenshots/
```

### Q: Video dosyaları çok büyük
A: `.gitignore`'da Raw_Video klasörleri hariç tutulmuş. Git LFS kullanabilirsiniz:
```powershell
git lfs install
git lfs track "*.mp4"
git add .gitattributes
```

### Q: Commit geçmişini silmek istiyorum
```powershell
# Tehlikeli! Yedek alın önce
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git remote add origin URL
git push -f origin main
```

## ✅ Kontrol Listesi

Yükleme sonrası kontrol edin:

- [ ] README.md düzgün görünüyor
- [ ] LICENSE dosyası var
- [ ] .gitignore çalışıyor (.venv yüklenmediyse ✓)
- [ ] About bölümü dolu
- [ ] Topics eklenmiş
- [ ] İlk release yapıldı
- [ ] Repository public/private ayarı doğru

## 🎉 Tebrikler!

Projeniz GitHub'da! Artık:
- ⭐ Star alabilirsiniz
- 🍴 Fork edilebilir
- 🐛 Issue açılabilir
- 🔀 Pull request alabilirsiniz
- 📈 Analytics görebilirsiniz

---

## 📞 Yardım

Sorun yaşarsanız:
- GitHub Docs: https://docs.github.com
- Git Docs: https://git-scm.com/doc

---

<div align="center">

**Başarılar! 🚀**

</div>
