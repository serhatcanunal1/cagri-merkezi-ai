#!/usr/bin/env python3
"""
Voice Call Center - Main Application
This module contains the core logic for the voice call center application.

Developed by Trivox Team:
- Serhatcan Ünal, Elif Zeynep Tosun, Meryem Gençali, Ali Buğrahan Budak

Features:
- Speech recognition and text-to-speech
- Customer data management
- Conversation history tracking
- Billing analysis and complaint handling
- AI-powered conversation classification

Çağrı Merkezi - Ana Uygulama
Bu modül sesli çağrı merkezi uygulamasının ana mantığını içerir.
"""

import os
import sys
from pathlib import Path
import time

# Config dosyasını import et
try:
    from config import *
except ImportError:
    # Eğer config dosyası bulunamazsa, basit path hesaplama yap
    def get_project_root():
        current_file = Path(__file__).resolve()
        if current_file.parent.name == 'scripts':
            return current_file.parent.parent
        return current_file.parent
    PROJECT_ROOT = get_project_root()

# Logging sistemini import et
try:
    import logging
    from logging_config import setup_logging, get_logger, log_network_error, log_audio_error, log_model_error, log_performance, log_system_status
    logger = setup_logging(logging.INFO)
except ImportError:
    print("Uyarı: logging_config.py bulunamadı. Basit logging kullanılacak.")
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('CagriMerkezi')

# Ses konfigürasyonunu import et
try:
    from voice_config import ses_yoneticisi, ses_profili_degistir, ses_ayari_guncelle
except ImportError:
    print("Uyarı: voice_config.py bulunamadı. Varsayılan ses ayarları kullanılacak.")
    ses_yoneticisi = None

# Müşteri popup modülünü import et
try:
    from customer_popup import show_musteri_popup
except ImportError:
    print("Uyarı: musteri_popup.py bulunamadı. Popup özelliği devre dışı.")
    show_musteri_popup = None

# Geçmiş görüşmeler modülünü import et
try:
    from conversation_history import gecmis_yoneticisi
except ImportError:
    print("Uyarı: conversation_history.py bulunamadı. Geçmiş görüşmeler özelliği devre dışı.")
    gecmis_yoneticisi = None

# FFmpeg ayarlarını yap
setup_ffmpeg_paths()

from pydub import AudioSegment
import json
import time
import wave
import speech_recognition as sr
from gtts import gTTS
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import pyaudio
from pydub.playback import play

class SesliCagriMerkezi:
    def __init__(self, ui=None, ses_profili="varsayilan"):
        self.ui = ui
        
        # Geçmiş görüşme yöneticisini başlat
        self.aktif_gorusme_id = None
    
        # Ses yöneticisini başlat
        if ses_yoneticisi:
            ses_profili_degistir(ses_profili)
            self.ses_ayarlari = ses_yoneticisi.aktif_profil
        else:
            # Varsayılan ayarlar
            self.ses_ayarlari = {
                "mikrofon_index": 0,
                "mikrofon_enerji_esigi": 4000,
                "mikrofon_dinleme_suresi": 20,
                "mikrofon_gecikme": 0.1,
                "ses_tanima_dili": "tr-TR",
                "ses_tanima_timeout": 20,
                "ses_tanima_phrase_time_limit": 10,
                "ses_tanima_ambient_noise_adjustment": True,
                "ses_tanima_dynamic_energy_threshold": True,
                "ses_tanima_pause_threshold": 0.8,
                "ses_tanima_non_speaking_duration": 0.5,
                "ses_tanima_phrase_threshold": 0.3
            }
        
        # Mikrofon ayarlarını uygula
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = self.ses_ayarlari.get("mikrofon_enerji_esigi", 4000)
        self.recognizer.dynamic_energy_threshold = self.ses_ayarlari.get("ses_tanima_dynamic_energy_threshold", True)
        self.recognizer.pause_threshold = self.ses_ayarlari.get("ses_tanima_pause_threshold", 0.8)
        self.recognizer.non_speaking_duration = self.ses_ayarlari.get("ses_tanima_non_speaking_duration", 0.5)
        self.recognizer.phrase_threshold = self.ses_ayarlari.get("ses_tanima_phrase_threshold", 0.3)
        
        self.microphone = sr.Microphone(device_index=self.ses_ayarlari.get("mikrofon_index", 0))
        
        # BERTurk modeli ve tokenizer - config'den al
        try:
            model_path = BERTURK_CAGRI_MODEL_DIR
            if not model_path.exists():
                print(f"Uyarı: Model dizini bulunamadı: {model_path}")
                print("Lütfen model dosyalarının doğru konumda olduğundan emin olun.")
                return
                
            self.model_bert = BertForSequenceClassification.from_pretrained(str(model_path))
            self.tokenizer = BertTokenizer.from_pretrained(str(model_path))
            self.model_bert.eval()  # Değerlendirme moduna al
        except Exception as e:
            print(f"Model yükleme hatası: {e}")
            return

        # Kategori isimleri ve yanıtları - config'den al
        self.kategoriler = KATEGORILER
    def yanit_fatura_itiraz(self, kullanici):
        son_4_ay = kullanici.get("son_4_aylik_kullanim", [])
        paket = kullanici.get("numaraya_tanimli_paket", {})

        if not son_4_ay or not paket:
            return "Kullanım ve paket bilgileri eksik."

        # Paket limitleri ve fiyatı dayanıklı okuma
        paket_fiyat = (
            paket.get("fiyatı")
            or paket.get("fiyati")
            or paket.get("fiyat")
            or 0
        )
        paket_dk_limit = int(paket.get("dakika", 0) or 0)
        paket_sms_limit = int(paket.get("sms", 0) or 0)

        # 'data_gb' alanı veride MB cinsinden olabildiği gibi (5000=5GB), bazı kayıtlarda GB da olabilir.
        # Sağlamlık için sezgisel dönüşüm: >=1024 ise MB varsay, aksi halde GB→MB çevir.
        data_field_value = paket.get("data_gb", 0) or 0
        try:
            data_field_value = float(data_field_value)
        except Exception:
            data_field_value = 0
        if data_field_value >= 1024:
            paket_data_limit_mb = int(data_field_value)
        else:
            paket_data_limit_mb = int(data_field_value * 1024)

        kampanya = kullanici.get("aktif_kampanya", {})
        kampanya_indirim = kampanya.get("indirimYüzdesi") or kampanya.get("indirimYuzdesi") or 0

        analiz_sonucu = []
        
        # SADECE SON AY (EN GÜNCEL FATURA) ANALİZİ
        if not son_4_ay:
            return "Fatura geçmişi bulunamadı."
            
        # En güncel ayı al (son eleman)
        son_ay = son_4_ay[-1]
        ay = son_ay.get("ay", "Bilinmiyor")
        odeme = float(son_ay.get("odeme_tl", 0) or 0)

        kullanilan_dk = int(son_ay.get("konusma_dakika", 0) or 0)
        kullanilan_sms = int(son_ay.get("sms", 0) or 0)
        kullanilan_data_mb = int(son_ay.get("data_mb", 0) or 0)
        yurtdisi_dk = int(
            son_ay.get("yurt_dişi_dakika")
            or son_ay.get("yurt_disi_dakika")
            or 0
        )

        sebepler = []
        if paket_dk_limit and kullanilan_dk > paket_dk_limit:
            sebepler.append(f"dakika aşımı (+{kullanilan_dk - paket_dk_limit} dk)")
        if paket_sms_limit and kullanilan_sms > paket_sms_limit:
            sebepler.append(f"SMS aşımı (+{kullanilan_sms - paket_sms_limit} SMS)")
        if paket_data_limit_mb and kullanilan_data_mb > paket_data_limit_mb:
            sebepler.append(f"internet aşımı (+{kullanilan_data_mb - paket_data_limit_mb} MB)")
        if yurtdisi_dk:
            sebepler.append(f"yurt dışı arama ({yurtdisi_dk} dk)")

        fark = odeme - float(paket_fiyat or 0)

        if fark > 0.01:
            # ÖNCE PAKET AŞIMI KONTROLÜ
            if sebepler:
                analiz_sonucu.append(
                    f"{ay} ayında {', '.join(sebepler)} nedeniyle yaklaşık +{fark:.2f} TL fazla fatura."
                )
            # AŞIM YOKSA ÇİFT FATURA KESİMİ KONTROLÜ
            elif paket_fiyat and odeme >= 2 * float(paket_fiyat) - 5:  # 5 TL tolerans
                analiz_sonucu.append(
                    f"{ay} ayında çift fatura kesimi tespit edildi. Ödenen tutar ({odeme:.2f} TL) ödenecek tutarın ({paket_fiyat} TL) 2 katıdır. Aynı dönemde iki kez faturalandırma yapılmış."
                )
            # DİĞER MUHTEMEL SEBEPLER
            else:
                muhtemel = []
                if kampanya_indirim:
                    muhtemel.append("kampanya/indirim değişikliği")
                if paket_fiyat and odeme >= 1.8 * float(paket_fiyat):
                    muhtemel.append("muhtemel çifte kesim")
                muhtemel.append("ek servis veya mobil ödeme")
                analiz_sonucu.append(
                    f"{ay} ayında paket aşımı görünmüyor; yaklaşık +{fark:.2f} TL ek ücret. Muhtemel sebep: {', '.join(muhtemel)}."
                )
        else:
            if sebepler:
                analiz_sonucu.append(
                    f"{ay} ayında {', '.join(sebepler)} tespit edildi; fatura tutarında artış görünmüyor."
                )

        if not analiz_sonucu:
            analiz_sonucu.append(f"{ay} ayında faturanız normal limitler içinde.")

        return "Fatura analiz sonucu:\n" + "\n".join(analiz_sonucu)
    
    def yanit_paket_kalan_hak(self, kullanici):
        kampanya = kullanici.get("numaraya_tanimli_paket", {})
        kalanlar = kullanici.get("kalan_kullanim_haklari", {})

    # Kampanya metni
        if kampanya:
            kampanya_text = (
                f"{kampanya.get('paketİsmi', 'İsimsiz Kampanya')} kampanyası, "
                f"{kampanya.get('gecerlilikTarihi', 'Süre belirtilmemiş')} tarihine kadar geçerlidir."
            )
        else:
            kampanya_text = "Aktif kampanya bulunmamaktadır."

    # Kalan haklar metni
        if kalanlar:
            kalan_text = (
                f"{kalanlar.get('kalanDakika', 0)} dakika, "
                f"{kalanlar.get('kalanSms', 0)} SMS, "
                f"{kalanlar.get('kalanİnternet', 0)} GB internet hakkınız kaldı."
            )
        else:
            kalan_text = "Kalan kullanım hakkı bilgisi bulunmamaktadır."

        return f"Aktif kampanya: {kampanya_text}\nKalan kullanım haklarınız: {kalan_text}"

    def yanit_yeni_paket_kampanya(self, kullanici):
        paketler = kullanici.get("gecis_yapilabilecek_paketler", [])

        if not paketler:
            return "Geçiş yapılabilecek paket bulunamadı."

        paket_listesi = []
        for paket in paketler:
            isim = paket.get("paketİsmi", "İsimsiz Paket")
            fiyat = paket.get("fiyatı", "Belirtilmemiş")
            artilar = paket.get("artiları", [])
            artilar_str = ", ".join(artilar) if artilar else "Ek özellik yok"
            paket_listesi.append(f"- {isim} ({fiyat} TL) — Artıları: {artilar_str}")

        yanit = "Geçiş yapabileceğiniz paketler:\n" + "\n".join(paket_listesi)
        return yanit

    def yanit_borc_odeme(self, kullanici):
        son_odeme = kullanici.get("son_odeme_tarihi", "")
        odendi_mi = kullanici.get("fatura_odendi_mi", None)

        if isinstance(odendi_mi, bool):  # True/False ise çevir
         odendi_text = "Ödendi" if odendi_mi is True else "Ödenmedi" if odendi_mi is False else "Bilinmiyor"
    
        yanit = f"Son ödeme tarihi: {son_odeme} olan faturanızın durumu {odendi_text}"
        return yanit


    def yanit_iptal_talebi(self, kullanici):
        return "İptal talebiniz alınmıştır, işleminiz en kısa sürede gerçekleştirilecektir."

    def yanit_teknik_ariza(self, kullanici):
        return "Teknik arıza kaydınız oluşturuldu. En kısa sürede dönüş sağlanacaktır."

    def yanit_sim_kart_sifre(self, kullanici):
        return self.sim_kart_sifre_cevapla(kullanici)

    def normalize_phone_number(self, phone):
        """Telefon numarasını normalize et"""
        if not phone:
            return phone
        # +90 önekini kaldır ve 0 ile başlat
        phone = str(phone).strip()
        if phone.startswith("+90"):
            phone = "0" + phone[3:]
        elif phone.startswith("90") and len(phone) == 12:
            phone = "0" + phone[2:]
        # Sadece rakamları al
        phone = ''.join(filter(str.isdigit, phone))
        # 0 ile başlamazsa 0 ekle
        if not phone.startswith("0") and len(phone) == 10:
            phone = "0" + phone
        return phone

    def seslendir(self, metin):
        start_time = time.time()
        
        # ÖNCE UI'DA YAZDIR
        if self.ui:
            self.ui.add_message("Temsilci", metin, "assistant")
        
        # Geçmiş görüşmeye mesaj ekle
        if gecmis_yoneticisi and self.aktif_gorusme_id:
            try:
                # Mevcut kategoriyi al
                current_kategori = None
                for gorusme in gecmis_yoneticisi.gorusmeler["gorusmeler"]:
                    if gorusme["id"] == self.aktif_gorusme_id:
                        current_kategori = gorusme.get("kategori")
                        break
                gecmis_yoneticisi.mesaj_ekle(self.aktif_gorusme_id, "Temsilci", metin, current_kategori)
            except Exception as e:
                logger.error(f"Geçmiş görüşmeye mesaj eklenirken hata: {e}")
        
        try:
            logger.info(f"Seslendirme başlatılıyor: '{metin[:50]}...'")
            
            # Ses ayarlarını al
            dil = self.ses_ayarlari.get("dil", "tr")
            hiz = self.ses_ayarlari.get("hiz", 1.0)
            ses_seviyesi = self.ses_ayarlari.get("ses_seviyesi", 1.0)
            ses_tipi = self.ses_ayarlari.get("ses_tipi", "gtts")
            ses_oynatma = self.ses_ayarlari.get("ses_oynatma", "pydub")
            
            logger.debug(f"Ses ayarları: dil={dil}, hız={hiz}, seviye={ses_seviyesi}, tip={ses_tipi}, oynatma={ses_oynatma}")
            
            # Geçici dosya oluştur
            if ses_yoneticisi:
                mp3_dosyasi = ses_yoneticisi.gecici_dosya_olustur()
            else:
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    mp3_dosyasi = fp.name
            
            logger.debug(f"Geçici dosya oluşturuldu: {mp3_dosyasi}")
            
            # Ses üretimi
            if ses_tipi == "gtts":
                from gtts import gTTS
                logger.debug("gTTS ile ses üretiliyor...")
                tts = gTTS(text=metin, lang=dil, slow=False)
                tts.save(mp3_dosyasi)
            else:
                # Diğer ses tipleri için varsayılan gTTS
                from gtts import gTTS
                logger.debug("Varsayılan gTTS ile ses üretiliyor...")
                tts = gTTS(text=metin, lang=dil, slow=False)
                tts.save(mp3_dosyasi)
            
            logger.debug(f"Ses dosyası oluşturuldu: {mp3_dosyasi}")
            
            # Ses oynatma
            try:
                if ses_oynatma == "pydub":
                    from pydub import AudioSegment
                    from pydub.playback import play
                    logger.debug("pydub ile ses oynatılıyor...")
                    sound = AudioSegment.from_mp3(mp3_dosyasi)
                    
                    # Ses seviyesi ayarı
                    if ses_seviyesi != 1.0:
                        sound = sound + (20 * (ses_seviyesi - 1.0))  # dB cinsinden ayar
                    
                    play(sound)
                elif ses_oynatma == "playsound":
                    from playsound import playsound
                    logger.debug("playsound ile ses oynatılıyor...")
                    playsound(mp3_dosyasi)
                else:
                    # Varsayılan pydub
                    from pydub import AudioSegment
                    from pydub.playback import play
                    logger.debug("Varsayılan pydub ile ses oynatılıyor...")
                    sound = AudioSegment.from_mp3(mp3_dosyasi)
                    play(sound)
                    
            except Exception as e:
                log_audio_error(logger, e, "Ses oynatma hatası")
                print(f"Ses oynatma hatası: {e}")
                if self.ui:
                    self.ui.add_message("Sistem", f"Ses oynatılamadı: {e}", "system")
            finally:
                # Geçici dosyayı temizle
                if ses_yoneticisi:
                    # Ses yöneticisi geçici dosyaları kendisi yönetir
                    pass
                else:
                    try:
                        os.remove(mp3_dosyasi)
                        logger.debug("Geçici dosya silindi")
                    except Exception as e:
                        logger.warning(f"Geçici dosya silinemedi: {e}")
                        
        except Exception as e:
            duration = time.time() - start_time
            log_audio_error(logger, e, f"Seslendirme hatası - Süre: {duration:.2f}s")
            print(f'Seslendirilemedi, hata: {e}')
            if self.ui:
                self.ui.add_message("Sistem", f"Seslendirilemedi: {e}", "system")
        
        duration = time.time() - start_time
        log_performance(logger, "Seslendirme", duration, f"Metin uzunluğu: {len(metin)}")

    def kategori_tahmin_et(self, metin):
        """BERTurk modeli ile kategori tahmini yap"""
        # Metni ön işleme: küçük harf, strip, noktalama kaldırma
        import re
        metin = metin.lower().strip()
        metin = re.sub(r'[.,!?;:()\[\]{}"]', '', metin)
        inputs = self.tokenizer(metin, padding='max_length', truncation=True, max_length=64, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model_bert(**inputs)
            tahmin = torch.argmax(outputs.logits, dim=1).item()
            prob = torch.softmax(outputs.logits, dim=1)[0]
            guven = prob[tahmin].item() * 100
        print(f"Tahmin edilen kategori: {tahmin} | Güven: %{guven:.2f} | Metin: {metin}")
        return tahmin, guven

    def dinle(self):
        """Google Speech Recognition ile dinleme yap"""
        with self.microphone as source:
            print("Konuşun...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            metin = self.recognizer.recognize_google(audio, language="tr-TR")
            return metin
        except sr.UnknownValueError:
            print("Ses anlaşılamadı")
            return None
        except sr.RequestError as e:
            print(f"Google Speech Recognition servisi hatası: {str(e)}")
            return None

    def mikrofondan_konusma_al(self, tekrar_sayisi=3):
        start_time = time.time()
        logger.info(f"Ses tanıma başlatılıyor - Deneme sayısı: {tekrar_sayisi}")
        
        if self.ui:
            self.ui.clear_status()
            self.ui.notify_speak()  # Sadece müşteri konuşma sırası başında bir kez
        
        # Ses ayarlarını al
        timeout = self.ses_ayarlari.get("ses_tanima_timeout", 20)
        phrase_time_limit = self.ses_ayarlari.get("ses_tanima_phrase_time_limit", 10)
        ambient_noise_adjustment = self.ses_ayarlari.get("ses_tanima_ambient_noise_adjustment", True)
        dil = self.ses_ayarlari.get("ses_tanima_dili", "tr-TR")
        
        logger.debug(f"Ses tanıma ayarları: timeout={timeout}, phrase_limit={phrase_time_limit}, ambient={ambient_noise_adjustment}, dil={dil}")
        
        for deneme in range(tekrar_sayisi):
            logger.info(f"Ses tanıma denemesi {deneme + 1}/{tekrar_sayisi}")
            
            with self.microphone as source:
                logger.debug("Mikrofon kaynağı açıldı")
                if ambient_noise_adjustment:
                    logger.debug("Arka plan gürültüsü ayarlanıyor...")
                    self.recognizer.adjust_for_ambient_noise(source)
                logger.debug("Dinleme başlatılıyor...")
                
                try:
                    audio = self.recognizer.listen(
                        source, 
                        timeout=timeout,
                        phrase_time_limit=phrase_time_limit
                    )
                    logger.debug("Ses kaydı başarıyla alındı")
                except sr.WaitTimeoutError:
                    logger.warning(f"Deneme {deneme + 1}: Dinleme zaman aşımı")
                    continue
                except Exception as e:
                    log_audio_error(logger, e, f"Ses kaydı hatası - Deneme {deneme + 1}")
                    continue
                
            try:
                logger.debug("Google Speech Recognition ile tanıma başlatılıyor...")
                text = self.recognizer.recognize_google(audio, language=dil)
                logger.info(f"Metin başarıyla tanındı: '{text[:50]}...'")
                
                # ÖNCE UI'DA YAZDIR
                if self.ui:
                    self.ui.add_message("Müşteri", text, "customer")
                
                # Geçmiş görüşmeye mesaj ekle
                if gecmis_yoneticisi and self.aktif_gorusme_id:
                    try:
                        # Mevcut kategoriyi al
                        current_kategori = None
                        for gorusme in gecmis_yoneticisi.gorusmeler["gorusmeler"]:
                            if gorusme["id"] == self.aktif_gorusme_id:
                                current_kategori = gorusme.get("kategori")
                                break
                        gecmis_yoneticisi.mesaj_ekle(self.aktif_gorusme_id, "Müşteri", text, current_kategori)
                    except Exception as e:
                        logger.error(f"Geçmiş görüşmeye müşteri mesajı eklenirken hata: {e}")
                
                duration = time.time() - start_time
                log_performance(logger, "Ses Tanıma", duration, f"Başarılı - Deneme: {deneme + 1}")
                return text
                
            except sr.UnknownValueError:
                logger.warning(f"Deneme {deneme + 1}: Ses anlaşılamadı")
                print('Lütfen tekrar deneyin.')
            except sr.RequestError as e:
                log_network_error(logger, e, f"Google Speech Recognition hatası - Deneme {deneme + 1}")
                print('Lütfen tekrar deneyin.')
            except Exception as e:
                log_audio_error(logger, e, f"Beklenmeyen ses tanıma hatası - Deneme {deneme + 1}")
                print('Lütfen tekrar deneyin.')
        
        duration = time.time() - start_time
        logger.error(f"Ses tanıma başarısız - Tüm denemeler tükendi - Toplam süre: {duration:.2f}s")
        print('Üzgünüm, sizi anlayamadım. Görüşme sonlandırılıyor.')
        return None

    def kullanici_bilgileri(self, telefon):
        """Kullanıcı bilgilerini getir"""
        try:
            with open(KULLANICI_FATURALAR_FILE, "r", encoding="utf-8") as f:
                veriler = json.load(f)
            # Numara normalize: 0 ile başlıyorsa +90 ekle, boşlukları ve tireleri kaldır
            tel_clean = ''.join(filter(str.isdigit, telefon))
            if tel_clean.startswith('0'):
                tel_plus90 = '+90' + tel_clean[1:]
            elif tel_clean.startswith('90'):
                tel_plus90 = '+' + tel_clean
            elif tel_clean.startswith('+90'):
                tel_plus90 = tel_clean
            else:
                tel_plus90 = '+90' + tel_clean[-10:]
            for kullanici in veriler:
                vt_tel = ''.join(filter(str.isdigit, kullanici["numara"]))
                vt_tel_plus90 = '+90' + vt_tel[-10:]
                if kullanici["numara"] == telefon or kullanici["numara"] == tel_plus90 or vt_tel_plus90 == tel_plus90:
                    return kullanici
            return None
        except Exception as e:
            print(f"Kullanıcı bilgileri hatası: {str(e)}")
            return None

    def fatura_analiz(self, kullanici):
        """Fatura analizi için yardımcı fonksiyon"""
        try:
            if kullanici:
                son_4_ay = kullanici["faturalar"][-4:]
                son_ay = son_4_ay[-1]
                onceki_aylar = son_4_ay[:-1]
                ortalama = sum([f["tutar"] for f in onceki_aylar]) / len(onceki_aylar)
                fark = son_ay["tutar"] - ortalama
                return {
                    "ad": kullanici["ad"],
                    "son_ay": son_ay,
                    "onceki_aylar": onceki_aylar,
                    "fark": fark,
                    "detay": son_ay["detay"],
                    "ekstra": son_ay["ekstra"],
                    "paket": son_ay["paket"]
                }
        except Exception as e:
            print(f"Fatura analizi hatası: {str(e)}")
            return None

    def telefon_numarasi_al(self):
        """Kullanıcıdan telefon numarası al"""
        self.seslendir("Telefon numaranızı söyler misiniz?")
        while True:
            telefon = self.dinle()
            if telefon and len(telefon.replace(" ", "")) >= 10:
                # Numarayı temizle ve formatla
                telefon = ''.join(filter(str.isdigit, telefon))
                if len(telefon) >= 10:
                    telefon = telefon[-10:]  # Son 10 haneyi al
                    return f"0{telefon}"
            self.seslendir("Geçerli bir telefon numarası söyleyin")

    def tespit_et_berturk(self, metin):
        import torch
        inputs = self.tokenizer(metin, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model_bert(**inputs)
            logits = outputs.logits
            predicted = torch.argmax(logits, dim=1).item()
        print(f"DEBUG: Tahmin edilen kategori: {predicted}")
        return predicted

    def kullanici_verisi_getir(self, telefon):
        import json
        try:
            with open(KULLANICI_FATURALAR_FILE, "r", encoding="utf-8") as f:
                veriler = json.load(f)
            for kullanici in veriler:
                vt_tel = ''.join(filter(str.isdigit, kullanici["numara"]))
                vt_tel_plus90 = '+90' + vt_tel[-10:]
                tel_clean = ''.join(filter(str.isdigit, telefon))
                if tel_clean.startswith('0'):
                    tel_plus90 = '+90' + tel_clean[1:]
                elif tel_clean.startswith('90'):
                    tel_plus90 = '+' + tel_clean
                elif tel_clean.startswith('+90'):
                    tel_plus90 = tel_clean
                else:
                    tel_plus90 = '+90' + tel_clean[-10:]
                if kullanici["numara"] == telefon or kullanici["numara"] == tel_plus90 or vt_tel_plus90 == tel_plus90:
                    return kullanici
            return None
        except Exception as e:
            print(f"DEBUG: Kullanıcı verisi alınamadı, hata: {e}")
            return None

    def fatura_itiraz_cevapla(self, kullanici_verisi):
        faturalar = kullanici_verisi.get("faturalar", [])
        paket = kullanici_verisi.get("paket", "")
        kullanimlar = kullanici_verisi.get("kullanimlar", [8, 9, 7, 12])
        ekstra_islem = kullanici_verisi.get("ekstra_islem", "")
        yanit = f"Son 4 aylık fatura tutarlarınız: {faturalar}.\n"
        yanit += f"Tanımlı paketiniz: {paket}.\n"
        yanit += f"Son 4 ayda veri kullanımlarınız (GB): {kullanimlar}.\n"
        if len(faturalar) == 4 and len(kullanimlar) == 4:
            if kullanimlar[-1] > kullanimlar[-2]:
                yanit += f"Son ayda ({kullanimlar[-1]} GB) önceki aya göre daha fazla veri kullanmışsınız. Fazla fatura sebebi: {ekstra_islem}."
            else:
                yanit += "Son ayda ekstra bir kullanım görünmüyor. Detaylı inceleme için müşteri temsilcisine bağlanabilirsiniz."
        else:
            yanit += "Fatura veya kullanım verileriniz eksik."
        return yanit

    def borc_sorgu_cevapla(self, kullanici_verisi):
        faturalar = kullanici_verisi.get("faturalar", [])
        son_odeme_tarihi = kullanici_verisi.get("son_odeme_tarihi", "")
        borc_durumu = kullanici_verisi.get("borc_durumu", "ödenmedi")
        ad = kullanici_verisi.get("ad", "")
        if faturalar:
            son_fatura = faturalar[-1]
            if borc_durumu == "ödenmedi":
                yanit = f"{ad}, son fatura tutarınız: {son_fatura} TL. Son ödeme tarihi: {son_odeme_tarihi}. Borcunuz bulunmaktadır."
            else:
                yanit = f"{ad}, son fatura tutarınız: {son_fatura} TL. Son ödeme tarihi: {son_odeme_tarihi}. Borcunuz bulunmamaktadır."
        else:
            yanit = "Fatura bilgileriniz bulunamadı."
        return yanit

    def sim_kart_sifre_cevapla(self, kullanici_verisi):
        tc = kullanici_verisi.get("tc", "")
        sim_sifre = kullanici_verisi.get("sim_sifre", "")
        self.seslendir("Lütfen TC kimlik numaranızın son iki hanesini söyleyin.")
        tc_son_iki = self.mikrofondan_konusma_al()
        tc_son_iki = ''.join(filter(str.isdigit, tc_son_iki))
        if tc and tc_son_iki == tc[-2:]:
            return f"Sim kart şifreniz: {sim_sifre}"
        else:
            return "TC kimlik numarası doğrulanamadı. Güvenlik nedeniyle şifre verilemiyor."

    def paket_degistir_cevapla(self, kullanici_verisi):
        paket = kullanici_verisi.get("paket", "")
        kampanya = kullanici_verisi.get("kampanya", "")
        paket_onerisi = kullanici_verisi.get("paket_onerisi", "")
        yanit = f"Mevcut paketiniz: {paket}.\n"
        yanit += f"Size özel kampanya: {kampanya}.\n"
        yanit += f"Geçiş yapabileceğiniz önerilen paket: {paket_onerisi}."
        return yanit

    def yeni_hizmet_cevapla(self, kullanici_verisi):
        kampanya = kullanici_verisi.get("kampanya", "")
        paket_onerisi = kullanici_verisi.get("paket_onerisi", "")
        yanit = f"Size özel kampanya: {kampanya}.\n"
        yanit += f"Önerilen yeni paket: {paket_onerisi}."
        return yanit

    def cagri_merkezi_baslat(self):
        try:
            # UI'da çağrı başlat
            if self.ui:
                self.ui.start_call()
                self.ui.add_message("Sistem", "Çağrı merkezi başlatıldı", "system")
            
            self.seslendir("Merhaba, Trivox Çağrı Hizmetlerine hoş geldiniz. Sizi Tanımak adına telefon numaranızı alabilir miyim?")
            telefon = self.mikrofondan_konusma_al()
            if not telefon:
                self.seslendir("Telefon numarası alınamadı. Lütfen tekrar deneyin.")
                return
            telefon = ''.join(filter(str.isdigit, telefon))
            if len(telefon) == 10:
                telefon = '0' + telefon
            self.seslendir("Bir saniye bekletiyorum...")
            kullanici_verisi = self.kullanici_verisi_getir(telefon)
            while not kullanici_verisi:
                self.seslendir("Numaranız sistemde bulunamadı. Lütfen tekrar telefon numaranızı söyleyin.")
                telefon = self.mikrofondan_konusma_al()
                telefon = ''.join(filter(str.isdigit, telefon))
                if len(telefon) == 10:
                    telefon = '0' + telefon
                self.seslendir("Bir saniye bekletiyorum...")
                kullanici_verisi = self.kullanici_verisi_getir(telefon)
            ad = kullanici_verisi.get("ad", "")
            self.seslendir(f"Sayın {ad}")
            
            # Telefon numarasını normalize et
            normalized_telefon = self.normalize_phone_number(telefon)
            
            # Yeni görüşme başlat
            if gecmis_yoneticisi:
                try:
                    self.aktif_gorusme_id = gecmis_yoneticisi.yeni_gorusme_baslat(normalized_telefon, ad)
                    print(f"Yeni görüşme başlatıldı: {self.aktif_gorusme_id}")
                    if self.ui:
                        self.ui.add_message("Sistem", f"Yeni görüşme başlatıldı - ID: {self.aktif_gorusme_id[:8]}...", "system")
                except Exception as e:
                    print(f"Görüşme başlatılırken hata: {e}")
            
            # Müşteri verilerini UI'ya gönder
            if self.ui:
                try:
                    # Kullanıcı verisine normalize edilmiş telefonu ekle
                    kullanici_verisi_copy = kullanici_verisi.copy()
                    kullanici_verisi_copy["normalized_numara"] = normalized_telefon
                    self.ui.set_musteri_data(kullanici_verisi_copy)
                    self.ui.add_message("Sistem", f"Müşteri tanındı: {ad} ({telefon})", "system")
                except Exception as e:
                    print(f"UI'ya müşteri verisi gönderilirken hata: {e}")
            
            self.sikayet_ve_destek_akisi(telefon, kullanici_verisi)
        except KeyboardInterrupt:
            self.seslendir("Görüşme sonlandırılıyor. Teşekkür eder İyi günler dileriz.")
        except Exception as e:
            print(f"Hata: {str(e)}")
            self.seslendir("Üzgünüm, bir hata oluştu.")

    def sikayet_ve_destek_akisi(self, telefon, kullanici_verisi):
        while True:
            self.seslendir("Size nasıl yardımcı olabilirim?")
            sikayet = self.mikrofondan_konusma_al()
            if not sikayet:
                self.seslendir("Üzgünüm, sizi anlayamadım. Lütfen hangi konuda yardım almak istediğinizi tekrar söyler misiniz?")
                continue
            kategori = self.tespit_et_berturk(sikayet)
            
            # Geçmiş görüşmeye kategori ekle
            if gecmis_yoneticisi and self.aktif_gorusme_id:
                try:
                    kategori_adi = self.kategoriler.get(kategori, "Bilinmiyor")
                    gecmis_yoneticisi.mesaj_ekle(self.aktif_gorusme_id, "Sistem", f"Kategori: {kategori_adi}", kategori_adi)
                    if self.ui:
                        self.ui.add_message("Sistem", f"Kategori tespit edildi: {kategori_adi}", "system")
                    gecmis_yoneticisi.kategori_guncelle(self.aktif_gorusme_id, kategori_adi)
                except Exception as e:
                    print(f"Geçmiş görüşmeye kategori eklenirken hata: {e}")
            
            if kategori in [0,1,2,3,4,5,6]:
                if kategori == 0:
                    yanit = self.yanit_fatura_itiraz(kullanici_verisi)
                elif kategori == 1:
                    paket = kullanici_verisi.get("numaraya_tanimli_paket", {})
                    paket_isim = paket.get("paketİsmi") or "paket adı bulunamadı"
                    kalanlar = kullanici_verisi.get("kalan_kullanim_haklari", {})
                    sikayet_lower = sikayet.lower()
                    if "son ay" in sikayet_lower:
                        yanit = self.paket_son_ay_cevapla(kullanici_verisi)
                    elif "son 2 ay" in sikayet_lower or "2 ay" in sikayet_lower:
                        yanit = self.paket_son_iki_ay_cevapla(kullanici_verisi)
                    elif "son 3 ay" in sikayet_lower or "3 ay" in sikayet_lower:
                        yanit = self.paket_son_uc_ay_cevapla(kullanici_verisi)
                    elif "sms" in sikayet_lower:
                        yanit = self.kalan_hak_tekil_cevapla(kalanlar, paket_isim, "sms")
                        if "anlaşılamadı" in yanit:
                            self.seslendir(yanit)
                            continue
                    elif "dakika" in sikayet_lower:
                        yanit = self.kalan_hak_tekil_cevapla(kalanlar, paket_isim, "dakika")
                        if "anlaşılamadı" in yanit:
                            self.seslendir(yanit)
                            continue
                    elif "internet" in sikayet_lower:
                        yanit = self.kalan_hak_tekil_cevapla(kalanlar, paket_isim, "internet")
                        if "anlaşılamadı" in yanit:
                            self.seslendir(yanit)
                            continue
                    elif "tüm hak" in sikayet_lower or "hepsi" in sikayet_lower or "kalan hak" in sikayet_lower:
                        yanit = self.yanit_paket_kalan_hak(kullanici_verisi)
                    else:
                        yanit = "Paket konusundaki talebiniz anlaşılamadı. Lütfen ne yapmak istediğinizi belirtir misiniz? Paket değiştirmek mi, kalan haklarınızı öğrenmek mi?"
                        self.seslendir(yanit)
                        # Tekrar talep al
                        continue
                elif kategori == 2:
                    yanit = self.yanit_borc_odeme(kullanici_verisi)
                elif kategori == 3:
                    yanit = self.yanit_iptal_talebi(kullanici_verisi)
                elif kategori == 4:
                    yanit = self.yanit_yeni_paket_kampanya(kullanici_verisi)
                elif kategori == 5:
                    yanit = self.yanit_teknik_ariza(kullanici_verisi)
                elif kategori == 6:
                    yanit = self.yanit_sim_kart_sifre(kullanici_verisi)
            else:
                yanit = "Talebiniz anlaşılamadı. Lütfen hangi konuda yardım almak istediğinizi açık bir şekilde belirtir misiniz? Örneğin: fatura itirazı, paket değişikliği, borç sorgulama..."
                self.seslendir(yanit)
                # Tekrar talep al
                continue
            
            # Çözüm sunuldu, şimdi devam edip etmeyeceğini sor
            self.seslendir(yanit)

            # Evet/Hayır cevabı alana kadar tekrar sor
            while True:
                self.seslendir("Farklı bir konuda destek ister misiniz?")
                cevap = self.mikrofondan_konusma_al()
                if not cevap:
                    self.seslendir("Cevabınız anlaşılamadı. Lütfen evet veya hayır olarak cevap verin.")
                    continue
                elif "evet" in cevap.lower():
                    break  # Döngüden çık, evet seçeneğine devam et
                elif "hayır" in cevap.lower() or "hayir" in cevap.lower():
                    # Görüşmeyi bitir
                    if gecmis_yoneticisi and self.aktif_gorusme_id:
                        try:
                            gecmis_yoneticisi.gorusme_bitir(self.aktif_gorusme_id, durum="tamamlandi")
                            print(f"Görüşme bitirildi: {self.aktif_gorusme_id}")
                        except Exception as e:
                            print(f"Görüşme bitirme hatası: {e}")
                    self.seslendir("Görüşme sonlandırılıyor. Teşekkür eder İyi günler dileriz.")
                    return  # Fonksiyondan çık
                else:
                    self.seslendir("Lütfen evet veya hayır olarak cevap verin.")
                    continue
            
            # Buraya sadece "evet" cevabı ile gelinir
            self.seslendir("Bu numara için mi devam edelim?")
            numara_cevap = self.mikrofondan_konusma_al()
            if numara_cevap and "evet" in numara_cevap.lower():
                continue  # Aynı numara ile yeni şikayet alınır
            else:
                self.seslendir("Lütfen yeni telefon numarasını söyleyin.")
                yeni_telefon = self.mikrofondan_konusma_al()
                yeni_telefon = ''.join(filter(str.isdigit, yeni_telefon))
                if len(yeni_telefon) == 10:
                    yeni_telefon = '0' + yeni_telefon
                self.seslendir("Bir saniye bekletiyorum...")
                yeni_kullanici_verisi = self.kullanici_verisi_getir(yeni_telefon)
                if yeni_kullanici_verisi:
                    telefon = yeni_telefon
                    kullanici_verisi = yeni_kullanici_verisi
                    continue  # Yeni numara ile yeni şikayet alınır
                else:
                    self.seslendir("Numara sistemde bulunamadı. Görüşme sonlandırılıyor.")
                    break  # Döngüden çık, görüşme sonlandır

    def paket_son_ay_cevapla(self, kullanici):
        # Son ay kullanım ve kalan haklar
        son_4_ay = kullanici.get("son_4_aylik_kullanim", [])
        if not son_4_ay:
            return "Son ay kullanım verisi bulunamadı."
        son_ay = son_4_ay[-1]
        metin = f"Son ay ({son_ay.get('ay', 'Bilinmiyor')}) kullanımınız: {son_ay.get('konusma_dakika', 0)} dakika, {son_ay.get('sms', 0)} SMS, {son_ay.get('data_mb', 0)/1024:.2f} GB internet."
        return metin

    def paket_son_iki_ay_cevapla(self, kullanici):
        son_4_ay = kullanici.get("son_4_aylik_kullanim", [])
        if not son_4_ay or len(son_4_ay) < 2:
            return "Son iki ay kullanım verisi bulunamadı."
        metin = "Son iki ay kullanımınız:\n"
        for ay_veri in son_4_ay[-2:]:
            metin += f"- {ay_veri.get('ay', 'Bilinmiyor')}: {ay_veri.get('konusma_dakika', 0)} dakika, {ay_veri.get('sms', 0)} SMS, {ay_veri.get('data_mb', 0)/1024:.2f} GB internet.\n"
        return metin
    
    def kalan_hak_tekil_cevapla(self, kalanlar, paket_isim, hak_tipi):
        if hak_tipi == "sms":
            sms = kalanlar.get("kalanSms", 0)
            return f"{paket_isim} paketinizden kalan SMS hakkınız: {sms} SMS'dir."
        elif hak_tipi == "dakika":
            dakika = kalanlar.get("kalanDakika", 0)
            return f"{paket_isim} paketinizden kalan dakika hakkınız: {dakika} dakikadır."
        elif hak_tipi == "internet":
            gb = kalanlar.get("kalanİnternet", 0)
            return f"{paket_isim} paketinizden kalan internet kullanımınız: {gb} GB'dir."
        else:
            return "Kalan hak konusundaki talebiniz anlaşılamadı. Lütfen SMS, dakika veya internet hakkınızdan hangisini öğrenmek istediğinizi belirtiniz."
        
    def paket_son_uc_ay_cevapla(self, kullanici):
        # Son 3 ay kullanım
        son_4_ay = kullanici.get("son_4_aylik_kullanim", [])
        if not son_4_ay or len(son_4_ay) < 3:
            return "Son 3 ay kullanım verisi bulunamadı."
        metin = "Son 3 ay kullanımınız:\n"
        for ay_veri in son_4_ay[-3:]:
            metin += f"- {ay_veri.get('ay', 'Bilinmiyor')}: {ay_veri.get('konusma_dakika', 0)} dakika, {ay_veri.get('sms', 0)} SMS, {ay_veri.get('data_mb', 0)/1024:.2f} GB internet.\n"
        return metin

if __name__ == "__main__":
    from ui_cagri_merkezi import CagriMerkeziUI
    ui = CagriMerkeziUI()
    cagri_merkezi = SesliCagriMerkezi(ui=ui)
    import threading
    threading.Thread(target=cagri_merkezi.cagri_merkezi_baslat, daemon=True).start()
    ui.run()
