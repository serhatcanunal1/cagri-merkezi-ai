# 🎯 AI Destekli Sesli Çağrı Merkezi Sistemi

## 📋 Proje Genel Bakış

**Proje Adı**: AI Voice Call Center System  
**Geliştirici**: Trivox Team  
**Takım Kaptanı**: Serhatcan Ünal (@serhatcanunal1)  
**GitHub Repository**: https://github.com/serhatcanunal1/cagri-merkezi-ai  
**Yarışma**: TEKNOFEST 2025 Türkçe Doğal Dil İşleme Yarışması - **Senaryo Kategorisi**  
**Lisans**: MIT License  
**Dil**: Türkçe  
**Teknoloji Stack**: Python, BERT, Speech Recognition, Tkinter, JSON, CSV

### 👥 Geliştirici Ekibi
- **Serhatcan Ünal** - Takım Kaptanı
- **Elif Zeynep Tosun** - AI & ML Geliştirici
- **Meryem Gençali** - Backend Geliştirici
- **Ali Buğrahan Budak** - Frontend & UI Geliştirici

---

## 🎯 Sistem Özellikleri

### ✅ **Desteklenen İşlemler**
- **Paket Değişikliği**: Mevcut paketi değiştirme, yeni paket önerileri
- **Fatura Sorgulama**: Fatura bilgileri, borç durumu, ödeme geçmişi
- **Teknik Destek**: Arıza bildirimi, teknik sorun çözümü
- **Müşteri Bilgileri**: Profil güncelleme, şifre değiştirme
- **SIM Card İşlemleri**: SIM kart aktivasyonu, PIN değiştirme

### 📊 **Performans Metrikleri**
- **Başarı Oranı**: %97
- **Müşteri Memnuniyeti**: 4.08/5
- **Ortalama Yanıt Süresi**: 0.023s
- **AI Model F1 Score**: 0.91

---

## 📞 Örnek Çağrı Diyalogları

### **📱 Test Numaraları ve Senaryolar**

#### **1. Paket Değişikliği Senaryosu**
**Test Numarası**: `5551234567`  
**TC Kimlik**: `12345678901`  
**PIN**: `1234`

```
Müşteri: "Merhaba, paketimi değiştirmek istiyorum"
Sistem: "Merhaba! Paket değişikliği için size yardımcı olabilirim. 
        TC kimlik numaranızın son iki hanesini söyler misiniz?"
Müşteri: "01"
Sistem: "Teşekkürler. Şimdi SIM kart PIN kodunuzu girer misiniz?"
Müşteri: "1234"
Sistem: "Doğrulama başarılı! Mevcut paketiniz: 50GB İnternet + 1000 DK
        Size uygun paketler: 100GB İnternet + 2000 DK (₺89.90),
        200GB İnternet + Sınırsız DK (₺129.90)"
Müşteri: "100GB'lık paketi istiyorum"
Sistem: "100GB İnternet + 2000 DK paketine geçiş yapılıyor...
        İşleminiz tamamlandı! Yeni paketiniz 1 saat içinde aktif olacak."
```

#### **2. Fatura Sorgulama Senaryosu**
**Test Numarası**: `5559876543`  
**TC Kimlik**: `98765432109`  
**PIN**: `5678`

```
Müşteri: "Faturamı öğrenmek istiyorum"
Sistem: "Fatura bilgilerinizi öğrenmek için TC kimlik numaranızın 
        son iki hanesini söyler misiniz?"
Müşteri: "09"
Sistem: "SIM kart PIN kodunuzu girer misiniz?"
Müşteri: "5678"
Sistem: "Doğrulama başarılı! Son faturanız: ₺89.90
        Son ödeme tarihi: 15 Aralık 2024
        Ödeme durumu: Ödenmedi
        Toplam borcunuz: ₺89.90"
Müşteri: "Ödeme yapabilir miyim?"
Sistem: "Evet, ödeme yapabilirsiniz. Kredi kartı ile ödeme için 1,
        Havale/EFT için 2'yi tuşlayın."
```

#### **3. Teknik Destek Senaryosu**
**Test Numarası**: `5551112233`  
**TC Kimlik**: `11122233344`  
**PIN**: `9999`

```
Müşteri: "İnternetim çalışmıyor, yardım eder misiniz?"
Sistem: "Teknik destek için size yardımcı olacağım. 
        TC kimlik numaranızın son iki hanesini söyler misiniz?"
Müşteri: "44"
Sistem: "SIM kart PIN kodunuzu girer misiniz?"
Müşteri: "9999"
Sistem: "Doğrulama başarılı! İnternet sorununuz için size yardımcı olacağım.
        Önce cihazınızı yeniden başlatmayı deneyin.
        Sorun devam ederse, size teknik ekibimizi yönlendireceğim."
Müşteri: "Yeniden başlattım ama çalışmıyor"
Sistem: "Anlıyorum. Teknik ekibimiz 2 saat içinde sizinle iletişime geçecek.
        Arıza numaranız: TK-2024-001234"
```

#### **4. SIM Card İşlemleri**
**Test Numarası**: `5554445566`  
**TC Kimlik**: `44455566677`  
**PIN**: `7777`

```
Müşteri: "SIM kartımı aktif etmek istiyorum"
Sistem: "SIM kart aktivasyonu için TC kimlik numaranızın 
        son iki hanesini söyler misiniz?"
Müşteri: "77"
Sistem: "Mevcut PIN kodunuzu girer misiniz?"
Müşteri: "7777"
Sistem: "Doğrulama başarılı! SIM kartınız zaten aktif durumda.
        PIN kodunuzu değiştirmek ister misiniz?"
Müşteri: "Evet, PIN kodumu değiştirmek istiyorum"
Sistem: "Yeni PIN kodunuzu 4 haneli olarak söyler misiniz?"
Müşteri: "8888"
Sistem: "PIN kodunuz başarıyla değiştirildi!"
```

---

## 🏗️ Sistem Mimarisi

### **Ana Bileşenler**
- **`run_call_center.py`**: Sistem başlatıcı
- **`scripts/voice_call_center.py`**: Ses işleme motoru (STT/TTS)
- **`scripts/mock_functions.py`**: Mock API fonksiyonları
- **`scripts/performance_metrics.py`**: KPI sistemi
- **`scripts/benchmark_tester.py`**: Test sistemi
- **`scripts/call_center_ui.py`**: Kullanıcı arayüzü

### **AI Model**
- **BERTurk**: Türkçe BERT tabanlı sınıflandırma
- **F1 Score**: 0.91 (Mükemmel performans)
- **7 Kategori**: Fatura, Paket, Borç, Yeni Paket, İptal, Teknik, SIM

---

## 🛠️ Kurulum ve Çalıştırma

### **Sistem Gereksinimleri**
- Python 3.8+
- Mikrofon ve hoparlör
- İnternet bağlantısı

### **Kurulum**
```bash
# Repository'yi klonlayın
git clone https://github.com/serhatcanunal1/cagri-merkezi-ai.git
cd cagri-merkezi-ai

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Sistemi çalıştırın
python run_call_center.py
```

### **Test Senaryoları**
```bash
# 100 test senaryosunu çalıştırın
python scripts/benchmark_tester.py

# Performans analizi
python scripts/performance_metrics.py
```

---

## 📊 Mock Fonksiyonlar

### **Desteklenen API Fonksiyonları**
- **`getUserInfo(user_id)`**: Müşteri bilgileri
- **`getAvailablePackages(user_id)`**: Uygun paketler
- **`initiatePackageChange(user_id, package_id)`**: Paket değişikliği
- **`getBillingInfo(user_id)`**: Fatura bilgileri
- **`validateCustomer(phone, tc, pin)`**: Müşteri doğrulama

### **Örnek Kullanım**
```python
# Müşteri bilgilerini al
user_info = getUserInfo("5551234567")
print(f"Müşteri: {user_info['name']} {user_info['surname']}")

# Uygun paketleri listele
packages = getAvailablePackages("5551234567")
for package in packages:
    print(f"{package['name']}: {package['price']}₺")
```

---

## 🎯 TEKNOFEST 2025 Uyumluluğu

### **✅ Karşılanan Gereksinimler**
- **STT/TTS Entegrasyonu**: Google Speech API + gTTS
- **Mock Fonksiyonlar**: 5 temel fonksiyon
- **Dinamik Araç Seçimi**: Kategori bazlı karar alma
- **Bağlam Yönetimi**: Görüşme geçmişi takibi
- **Çok Adımlı Karar Zincirleri**: TC kimlik + PIN doğrulama
- **KPI Sistemi**: Performans ölçümleme
- **100 Test Senaryosu**: Benchmark sistemi

### **📈 Performans Sonuçları**
- **Başarı Oranı**: %97 (97/100 test)
- **Müşteri Memnuniyeti**: 4.08/5
- **Ortalama Yanıt Süresi**: 0.023s
- **Sistem Güvenilirliği**: %97

---

## 📞 İletişim

- **GitHub**: https://github.com/serhatcanunal1/cagri-merkezi-ai
- **Takım Kaptanı**: Serhatcan Ünal (@serhatcanunal1)
- **Dokümantasyon**: `SYSTEM_ARCHITECTURE.md`

---

## 📝 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır.

---

*Bu README dosyası, TEKNOFEST 2025 Türkçe Doğal Dil İşleme Yarışması - Senaryo Kategorisi gereksinimlerine uygun olarak hazırlanmıştır.*