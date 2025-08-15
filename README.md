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

## 🎯 TEKNOFEST 2025 Teknik Şartname Uyumluluğu

### ✅ **TAM KARŞILANAN GEREKSİNİMLER**

| **Gereksinim** | **Durum** | **Açıklama** | **Dosya/Modül** |
|----------------|-----------|--------------|-----------------|
| **STT/TTS Entegrasyonu** | ✅ Tam | Google Speech API + gTTS | `voice_call_center.py` |
| **Mock Fonksiyonlar** | ✅ Tam | getUserInfo, getAvailablePackages, initiatePackageChange | `mock_functions.py` |
| **Dinamik Araç Seçimi** | ✅ Tam | Kategori bazlı fonksiyon çağrıları | `voice_call_center.py` |
| **Bağlam Yönetimi** | ✅ Tam | Görüşme geçmişi ve durum takibi | `conversation_history.py` |
| **Çok Adımlı Karar Zincirleri** | ✅ Tam | TC kimlik, şifre doğrulama | `voice_call_center.py` |
| **Hata İşleme** | ✅ Tam | Kapsamlı hata yönetimi | Tüm modüller |
| **KPI Sistemi** | ✅ Tam | Performans ölçümleme | `performance_metrics.py` |
| **100 Örnek Test** | ✅ Tam | Benchmark sistemi | `benchmark_tester.py` |
| **Açık Kaynak** | ✅ Tam | MIT Lisansı | `LICENSE` |
| **Agentic Framework** | ✅ Tam | Dinamik karar alma | `voice_call_center.py` |
| **Durum Yönetimi** | ✅ Tam | Bellek mekanizmaları | `conversation_history.py` |
| **Harici Sistem Simülasyonu** | ✅ Tam | Mock API'ler | `mock_functions.py` |

### 📊 **BENCHMARK SONUÇLARI (100 Test)**

| **Metrik** | **Değer** | **Durum** | **Teknik Şartname Gereksinimi** |
|------------|-----------|-----------|----------------------------------|
| **Toplam Test** | 100/100 | ✅ Tamamlandı | ✅ 100 farklı zorluk seviyesi |
| **Başarı Oranı** | %97 | ✅ Mükemmel | ✅ %90+ hedefi aşıldı |
| **Müşteri Memnuniyeti** | 4.08/5 | ✅ Yüksek | ✅ 4.0+ hedefi aşıldı |
| **Ortalama Yanıt Süresi** | 0.023s | ✅ Hızlı | ✅ <1s hedefi aşıldı |
| **Sistem Güvenilirliği** | %97 | ✅ Güvenilir | ✅ %95+ hedefi aşıldı |
| **Hata Oranı** | %3 | ✅ Düşük | ✅ %5- hedefi aşıldı |

### 🎯 **SENARYO PERFORMANSI**

| **Senaryo Türü** | **Test Sayısı** | **Başarı Oranı** | **Ortalama Süre** | **Memnuniyet** | **Teknik Şartname Uyumu** |
|------------------|-----------------|------------------|-------------------|----------------|---------------------------|
| **Paket Değişikliği** | 40 | %92.5 | 0.022s | 4.08/5 | ✅ Temsili Senaryo |
| **Fatura Sorgulama** | 30 | %100 | 0.025s | 4.07/5 | ✅ Ek Senaryo |
| **Teknik Destek** | 20 | %100 | 0.020s | 4.10/5 | ✅ Ek Senaryo |
| **Bağlam Değişimi** | 10 | %100 | 0.026s | 4.10/5 | ✅ Zorluk Testi |

---

## 🏗️ Sistem Mimarisi

### **Katmanlı Mimari Yapısı**

```
┌─────────────────────────────────────────────────────────────┐
│                    KULLANICI ARAYÜZÜ KATMANI               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Tkinter UI    │  │   Ses Kontrolü  │  │   Loglar     │ │
│  │   (call_center_ │  │   (voice_config │  │   (logs/)    │ │
│  │    _ui.py)      │  │    .py)         │  │              │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    ANA KONTROL KATMANI                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   run_call_     │  │   Ses İşleme    │  │   Konfigü    │ │
│  │   center.py     │  │   (voice_call_  │  │   (config.py)│ │
│  │                 │  │    center.py)   │  │              │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI VE İŞLEME KATMANI                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   BERT Model    │  │   Mock Functions │  │   Performance│ │
│  │   (models/)     │  │   (mock_functions│  │   Metrics    │ │
│  │                 │  │    .py)         │  │   (performance│ │
│  └─────────────────┘  └─────────────────┘  │   _metrics.py)│ │
│  ┌─────────────────┐  ┌─────────────────┐  └──────────────┘ │
│  │   Conversation  │  │   Benchmark     │                  │
│  │   History       │  │   Tester        │                  │
│  │   (conversation_│  │   (benchmark_   │                  │
│  │    history.py)  │  │    tester.py)   │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    VERİ KATMANI                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   JSON Data     │  │   CSV Data      │  │   Model      │ │
│  │   (data/)       │  │   (data/)       │  │   Files      │ │
│  │                 │  │                 │  │   (models/)  │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Bileşen Detayları

### **1. Ana Kontrol Katmanı**

#### `run_call_center.py` - Sistem Başlatıcı
- **Amaç**: Sistem koordinatörü ve başlatıcı
- **Sorumluluklar**:
  - ✅ Bağımlılık kontrolü ve doğrulama
  - ✅ Dosya varlığı kontrolü
  - ✅ Sistem başlatma ve koordinasyon
  - ✅ Hata yönetimi ve loglama
  - ✅ Performans izleme

#### `scripts/voice_call_center.py` - Ses İşleme Motoru
- **Amaç**: Ana AI ve ses işleme motoru
- **Sorumluluklar**:
  - ✅ **STT (Speech-to-Text)**: Google Speech API entegrasyonu
  - ✅ **TTS (Text-to-Speech)**: gTTS ile Türkçe ses sentezi
  - ✅ **BERT Sınıflandırma**: Türkçe BERT tabanlı konuşma analizi (F1: 0.91)
  - ✅ **Akıllı Yanıt Sistemi**: Bağlama duyarlı yanıtlar
  - ✅ **Performans Loglama**: Detaylı performans takibi
  - ✅ **Dinamik Araç Seçimi**: Kategori bazlı fonksiyon çağrıları

### **2. AI ve İşleme Katmanı**

#### `scripts/mock_functions.py` - Mock API Sistemi
**Teknik Şartname Gereksinimi**: Harici sistem simülasyonu

- **`getUserInfo(user_id)`**: Müşteri bilgileri sorgulama
  - ✅ Kullanıcı adı, soyadı, paket bilgisi
  - ✅ Sözleşme bitiş tarihi, ödeme durumu
  - ✅ Hata yönetimi ve doğrulama

- **`getAvailablePackages(user_id)`**: Uygun paket listesi
  - ✅ Müşteri durumuna göre filtreleme
  - ✅ Fiyat, hız, özellik bilgileri
  - ✅ Kısıtlama kontrolü

- **`initiatePackageChange(user_id, package_id)`**: Paket değişikliği
  - ✅ Sözleşme kontrolü
  - ✅ Ödeme durumu kontrolü
  - ✅ İşlem onayı ve aktivasyon

- **`getBillingInfo(user_id)`**: Fatura bilgileri
  - ✅ Son faturalar ve durumları
  - ✅ Toplam borç hesaplama
  - ✅ Ödeme geçmişi

- **`validateCustomer(phone, tc, pin)`**: Müşteri doğrulama
  - ✅ TC kimlik son iki hane kontrolü
  - ✅ SIM kart PIN doğrulama
  - ✅ Güvenlik kontrolleri

#### `scripts/performance_metrics.py` - KPI Sistemi
**Teknik Şartname Gereksinimi**: Performans ölçümleme

- **Görüşme Metrikleri**:
  - ✅ Başarı oranı hesaplama
  - ✅ Müşteri memnuniyeti takibi
  - ✅ Ortalama görüşme süresi
  - ✅ Hata oranı analizi

- **Sistem Metrikleri**:
  - ✅ Toplam görüşme sayısı
  - ✅ Başarılı/başarısız görüşmeler
  - ✅ Sistem güvenilirliği
  - ✅ Eş zamanlı görüşme kapasitesi

#### `scripts/benchmark_tester.py` - Benchmark Sistemi
**Teknik Şartname Gereksinimi**: 100 farklı zorluk seviyesinde test

- **Test Senaryoları**:
  - ✅ **40 Paket Değişikliği Testi**: Easy, Medium, Hard, Expert
  - ✅ **30 Fatura Sorgulama Testi**: Easy, Medium, Hard, Expert
  - ✅ **20 Teknik Destek Testi**: Easy, Medium, Hard, Expert
  - ✅ **10 Bağlam Değişimi Testi**: Medium, Hard, Expert

- **Zorluk Seviyeleri**:
  - **Easy**: Basit, doğrudan işlemler
  - **Medium**: Orta karmaşıklık, ek kontroller
  - **Hard**: Yüksek karmaşıklık, çoklu adımlar
  - **Expert**: En karmaşık, bağlam değişimi dahil

### **3. Kullanıcı Arayüzü Katmanı**

#### `scripts/call_center_ui.py` - Modern UI
- **Amaç**: Tkinter tabanlı modern kullanıcı arayüzü
- **Özellikler**:
  - ✅ Gerçek zamanlı görüşme takibi
  - ✅ Müşteri arama ve filtreleme
  - ✅ Ses ayarları kontrolü
  - ✅ Log görüntüleme ve analiz
  - ✅ Performans dashboard'u

#### `scripts/voice_config.py` - Ses Konfigürasyonu
- **Amaç**: Ses ayarları yönetimi
- **Özellikler**:
  - ✅ Ses profili değiştirme
  - ✅ Hız ayarları (yavaş, normal, hızlı)
  - ✅ Kalite optimizasyonu
  - ✅ Ses cihazı seçimi

### **4. Veri Yönetimi Katmanı**

#### `data/` Klasörü
- **`kullanici_faturalar.json`**: Müşteri fatura verileri
- **`sikayetler.csv`**: Şikayet ve eğitim verileri
- **`train_berturk.jsonl`**: BERT eğitim verisi
- **`conversation_history.json`**: Görüşme geçmişi
- **`berturk_egitim_verisi_10664_7kategori.csv`**: Birleştirilmiş eğitim verisi (10,664 örnek, 7 kategori)
- **`berturk_egitim_verisi_ozeti.json`**: Eğitim verisi özeti ve istatistikler

#### `models/` Klasörü
- **BERT Modeli**: Türkçe BERT tabanlı sınıflandırma (F1: 0.91, Accuracy: 0.9017)
- **Konfigürasyon**: Model ayarları ve tokenizer
- **Eğitim Verisi**: Fine-tuning için hazır veri (10,664 test örneği)
- **Model Performansı**: 7 kategori, mükemmel sınıflandırma

---

## 🤖 AI Model Performans Analizi

### **BERTurk Çağrı Merkezi Modeli - Detaylı Sonuçlar**

**Model Mimarisi**: BERTurk (Turkish BERT) + Classification Head  
**Eğitim Verisi**: 10,664 test örneği  
**Kategori Sayısı**: 7  
**Test Set Boyutu**: 10,664  

#### **Kategori Bazlı F1 Skorları**

| **Kategori** | **F1 Score** | **Precision** | **Recall** | **Support** | **Durum** |
|--------------|--------------|---------------|------------|-------------|-----------|
| **Fatura İtirazı** | 0.92 | 0.93 | 0.91 | 1,900 | ✅ Mükemmel |
| **Paket Kalan Sorgulama** | 0.92 | 0.92 | 0.93 | 1,850 | ✅ Mükemmel |
| **Borç Sorgulama** | 0.91 | 0.91 | 0.92 | 1,800 | ✅ Mükemmel |
| **Yeni Paket/Kampanya Talebi** | 0.91 | 0.92 | 0.90 | 1,700 | ✅ Mükemmel |
| **İptal Talebi** | 0.89 | 0.90 | 0.89 | 1,750 | ✅ Yüksek |
| **Teknik Arıza** | 0.87 | 0.88 | 0.86 | 850 | ✅ Yüksek |
| **SIM Card/Şifre İşlemleri** | 0.86 | 0.87 | 0.85 | 814 | ✅ Yüksek |

#### **Genel Model Metrikleri**

| **Metrik** | **Değer** | **Durum** | **Açıklama** |
|------------|-----------|-----------|--------------|
| **Accuracy** | 0.9017 | ✅ Mükemmel | %90.17 doğruluk oranı |
| **Weighted F1** | 0.91 | ✅ Mükemmel | Ağırlıklı F1 skoru |
| **Macro Avg F1** | 0.90 | ✅ Mükemmel | Makro ortalama F1 |
| **Macro Avg Precision** | 0.90 | ✅ Mükemmel | Makro ortalama precision |
| **Macro Avg Recall** | 0.89 | ✅ Yüksek | Makro ortalama recall |

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

#### **5. Borç Sorgulama Senaryosu**
**Test Numarası**: `5557778899`  
**TC Kimlik**: `77788899900`  
**PIN**: `5555`

```
Müşteri: "Borç durumumu öğrenmek istiyorum"
Sistem: "Borç sorgulama için TC kimlik numaranızın 
        son iki hanesini söyler misiniz?"
Müşteri: "00"
Sistem: "SIM kart PIN kodunuzu girer misiniz?"
Müşteri: "5555"
Sistem: "Doğrulama başarılı! Borç durumunuz:
        Güncel faturanız: ₺89.90 (Son ödeme: 20 Aralık)
        Eski borçlarınız: ₺0.00
        Toplam borcunuz: ₺89.90"
Müşteri: "Taksitli ödeme yapabilir miyim?"
Sistem: "Evet, 3 taksit halinde ödeme yapabilirsiniz.
        Aylık taksit tutarı: ₺29.97"
```

#### **6. Yeni Paket Talebi**
**Test Numarası**: `5553334455`  
**TC Kimlik**: `33344455566`  
**PIN**: `4444`

```
Müşteri: "Yeni bir paket almak istiyorum"
Sistem: "Yeni paket talebi için TC kimlik numaranızın 
        son iki hanesini söyler misiniz?"
Müşteri: "66"
Sistem: "SIM kart PIN kodunuzu girer misiniz?"
Müşteri: "4444"
Sistem: "Doğrulama başarılı! Size özel kampanyalarımız:
        1. 150GB İnternet + Sınırsız DK (₺99.90/ay)
        2. 250GB İnternet + Sınırsız DK (₺129.90/ay)
        3. 500GB İnternet + Sınırsız DK (₺159.90/ay)"
Müşteri: "150GB'lık paketi istiyorum"
Sistem: "150GB İnternet + Sınırsız DK paketi seçildi.
        Aylık ücret: ₺99.90
        Aktivasyon ücreti: ₺0.00
        Paketiniz 24 saat içinde aktif olacak."
```

#### **7. İptal Talebi**
**Test Numarası**: `5556667788`  
**TC Kimlik**: `66677788899`  
**PIN**: `3333`

```
Müşteri: "Hattımı iptal etmek istiyorum"
Sistem: "Hattınızı iptal etmek için TC kimlik numaranızın 
        son iki hanesini söyler misiniz?"
Müşteri: "99"
Sistem: "SIM kart PIN kodunuzu girer misiniz?"
Müşteri: "3333"
Sistem: "Doğrulama başarılı! İptal talebiniz için size yardımcı olacağım.
        Mevcut sözleşmeniz: 15 Ocak 2025'e kadar geçerli
        İptal ücreti: ₺50.00
        Kalan borcunuz: ₺89.90"
Müşteri: "İptal etmek istiyorum"
Sistem: "İptal talebiniz kaydedildi. 30 gün içinde hattınız kapatılacak.
        İptal numaranız: IP-2024-005678"
```

---

## 🔄 Veri Akışı ve İşlem Süreci

### **1. Görüşme Başlatma Süreci**
```
Kullanıcı Girişi → UI Kontrolü → Sistem Başlatma → Ses İşleme → STT → BERT Analizi → Yanıt Oluşturma → TTS → Kullanıcı Çıkışı
```

### **2. Mock Fonksiyon Çağrı Süreci**
```
BERT Sınıflandırma → Kategori Belirleme → Mock Function Seçimi → API Çağrısı → Sonuç İşleme → Yanıt Oluşturma → Kullanıcıya İletim
```

### **3. Performans Takip Süreci**
```
Her İşlem → Performance Tracker → Metrics Hesaplama → KPI Analizi → Rapor Oluşturma → Dashboard Güncelleme
```

---

## 🛠️ Kurulum ve Çalıştırma

### **Sistem Gereksinimleri**
- Python 3.8+
- Windows 10/11, Linux, macOS
- Mikrofon ve hoparlör
- İnternet bağlantısı (Google API'ler için)

### **Kurulum Adımları**

#### **1. Bağımlılıkları Yükleme**
```bash
# Proje dizinine git
cd CagriMerkezi

# Gerekli paketleri yükle
pip install -r requirements.txt
```

#### **2. Sistem Başlatma**
```bash
# Ana sistemi başlat
python run_call_center.py
```

#### **3. Benchmark Testleri**
```bash
# 100 test senaryosunu çalıştır
python scripts/benchmark_tester.py
```

#### **4. Performans Analizi**
```bash
# Performans raporlarını görüntüle
python scripts/performance_metrics.py
```

### **Konfigürasyon Dosyaları**
- `config.py`: Sistem ayarları
- `voice_config.py`: Ses ayarları
- `logging_config.py`: Log ayarları

---

## 🔒 Güvenlik ve Veri Yönetimi

### **Veri Güvenliği**
- ✅ Müşteri verileri şifrelenmiş JSON formatında
- ✅ TC kimlik ve şifre bilgileri hash'lenmiş
- ✅ Log dosyaları güvenli erişim
- ✅ Veri sızıntısı koruması

### **Sistem Güvenliği**
- ✅ Mock fonksiyonlar güvenli API çağrıları
- ✅ Hata durumlarında veri koruması
- ✅ Güvenli dosya işlemleri
- ✅ Input validation ve sanitization

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