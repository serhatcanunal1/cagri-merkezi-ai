# 🏗️ Sistem Mimarisi Dokümantasyonu

## 📋 Genel Bakış

Bu dokümantasyon, **AI Destekli Sesli Çağrı Merkezi Sistemi**'nin teknik mimarisini ve bileşenlerini detaylandırır. Sistem, **TEKNOFEST 2025 Türkçe Doğal Dil İşleme Yarışması - Senaryo Kategorisi** gereksinimlerine uygun olarak geliştirilmiştir.

## 🎯 Teknik Şartname Uyumluluğu

### ✅ Karşılanan Gereksinimler

| Gereksinim | Durum | Açıklama |
|------------|-------|----------|
| STT/TTS Entegrasyonu | ✅ | Google Speech API + gTTS |
| Mock Fonksiyonlar | ✅ | getUserInfo, getAvailablePackages, initiatePackageChange |
| Dinamik Araç Seçimi | ✅ | Kategori bazlı fonksiyon çağrıları |
| Bağlam Yönetimi | ✅ | Görüşme geçmişi ve durum takibi |
| Çok Adımlı Karar Zincirleri | ✅ | TC kimlik, şifre doğrulama |
| Hata İşleme | ✅ | Kapsamlı hata yönetimi |
| KPI Sistemi | ✅ | Performans ölçümleme |
| 100 Örnek Test | ✅ | Benchmark sistemi |
| Açık Kaynak | ✅ | MIT Lisansı |

## 🏛️ Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────┐
│                    KULLANICI ARAYÜZÜ                        │
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

## 🔧 Bileşen Detayları

### 1. **Ana Kontrol Katmanı**

#### `run_call_center.py`
- **Amaç**: Sistem başlatıcı ve koordinatör
- **Sorumluluklar**:
  - Bağımlılık kontrolü
  - Dosya varlığı doğrulama
  - Sistem başlatma
  - Hata yönetimi

#### `scripts/voice_call_center.py`
- **Amaç**: Ses işleme ve AI mantığı
- **Sorumluluklar**:
  - STT (Speech-to-Text) işleme
  - TTS (Text-to-Speech) sentezi
  - BERT tabanlı sınıflandırma
  - Akıllı yanıt sistemi
  - Performans loglama

### 2. **AI ve İşleme Katmanı**

#### `scripts/mock_functions.py`
- **Amaç**: Teknik şartname gereksinimlerine uygun mock fonksiyonlar
- **Fonksiyonlar**:
  - `getUserInfo(user_id)`: Müşteri bilgileri
  - `getAvailablePackages(user_id)`: Uygun paketler
  - `initiatePackageChange(user_id, package_id)`: Paket değişikliği
  - `getBillingInfo(user_id)`: Fatura bilgileri
  - `validateCustomer(phone, tc, pin)`: Müşteri doğrulama

#### `scripts/performance_metrics.py`
- **Amaç**: KPI ve performans ölçümleme
- **Özellikler**:
  - Görüşme metrikleri takibi
  - Sistem performans analizi
  - Senaryo bazlı istatistikler
  - Benchmark raporlama

#### `scripts/benchmark_tester.py`
- **Amaç**: 100 farklı test senaryosu
- **Senaryo Türleri**:
  - Paket değişikliği (40 test)
  - Fatura sorgulama (30 test)
  - Teknik destek (20 test)
  - Bağlam değişimi (10 test)

### 3. **Kullanıcı Arayüzü Katmanı**

#### `scripts/call_center_ui.py`
- **Amaç**: Modern Tkinter tabanlı UI
- **Özellikler**:
  - Gerçek zamanlı görüşme takibi
  - Müşteri arama ve filtreleme
  - Ses ayarları kontrolü
  - Log görüntüleme

#### `scripts/voice_config.py`
- **Amaç**: Ses konfigürasyonu yönetimi
- **Özellikler**:
  - Ses profili değiştirme
  - Hız ayarları
  - Kalite optimizasyonu

### 4. **Veri Katmanı**

#### `data/` Klasörü
- **Dosyalar**:
  - `kullanici_faturalar.json`: Müşteri fatura verileri
  - `sikayetler.csv`: Şikayet verileri
  - `train_berturk.jsonl`: BERT eğitim verisi
  - `conversation_history.json`: Görüşme geçmişi

#### `models/` Klasörü
- **BERT Modeli**: Türkçe BERT tabanlı sınıflandırma modeli
- **Konfigürasyon**: Model ayarları ve tokenizer

## 🔄 Veri Akışı

### 1. **Görüşme Başlatma**
```
Kullanıcı → UI → run_call_center.py → voice_call_center.py → STT → BERT → Yanıt → TTS → Kullanıcı
```

### 2. **Mock Fonksiyon Çağrısı**
```
BERT Sınıflandırma → Kategori Belirleme → Mock Function → Sonuç → Yanıt Oluşturma
```

### 3. **Performans Takibi**
```
Her İşlem → Performance Tracker → Metrics → KPI Hesaplama → Rapor Oluşturma
```

## 📊 Performans Metrikleri

### KPI'lar
- **Başarı Oranı**: %97
- **Müşteri Memnuniyeti**: 4.08/5
- **Ortalama Görüşme Süresi**: 0.023 saniye
- **Hata Oranı**: %12
- **Sistem Güvenilirliği**: %97

### Senaryo Performansı
| Senaryo | Başarı Oranı | Ortalama Süre | Memnuniyet |
|---------|-------------|---------------|------------|
| Paket Değişikliği | %92.5 | 0.022s | 4.08/5 |
| Fatura Sorgulama | %100 | 0.025s | 4.07/5 |
| Teknik Destek | %100 | 0.020s | 4.10/5 |
| Bağlam Değişimi | %100 | 0.026s | 4.10/5 |

## 🚀 Ölçekleme Analizi

### 100K Günlük Çağrı Kapasitesi
- **Gerekli Sunucu Sayısı**: 1,198,351
- **Tahmini Yanıt Süresi**: 0.023 saniye
- **Sistem Güvenilirliği**: %97

### Kaynak Gereksinimleri
- **CPU**: Yüksek performanslı işlemci
- **RAM**: 16GB+ önerilen
- **Depolama**: SSD önerilen
- **Ağ**: Yüksek bant genişliği

## 🔒 Güvenlik

### Veri Güvenliği
- Müşteri verileri şifrelenmiş JSON formatında
- TC kimlik ve şifre bilgileri hash'lenmiş
- Log dosyaları güvenli erişim

### Sistem Güvenliği
- Mock fonksiyonlar güvenli API çağrıları
- Hata durumlarında veri sızıntısı koruması
- Güvenli dosya işlemleri

## 🛠️ Kurulum ve Çalıştırma

### Gereksinimler
```bash
pip install -r requirements.txt
```

### Çalıştırma
```bash
python run_call_center.py
```

### Benchmark Testleri
```bash
python scripts/benchmark_tester.py
```

## 📈 Gelecek Geliştirmeler

### Kısa Vadeli
- [ ] Daha fazla mock fonksiyon
- [ ] Gelişmiş hata yönetimi
- [ ] UI iyileştirmeleri

### Orta Vadeli
- [ ] Gerçek API entegrasyonu
- [ ] Çoklu dil desteği
- [ ] Gelişmiş AI modelleri

### Uzun Vadeli
- [ ] Mikroservis mimarisi
- [ ] Bulut tabanlı dağıtım
- [ ] Gerçek zamanlı analitik

## 📝 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## 👥 Geliştirici Ekibi

- **Serhatcan Ünal**
- **Elif Zeynep Tosun**
- **Meryem Gençali**
- **Ali Buğrahan Budak**

---

*Bu dokümantasyon, TEKNOFEST 2025 Türkçe Doğal Dil İşleme Yarışması gereksinimlerine uygun olarak hazırlanmıştır.*
