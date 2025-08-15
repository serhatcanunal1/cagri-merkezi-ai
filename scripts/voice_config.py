"""
Çağrı Merkezi Ses Konfigürasyon Dosyası
Bu dosya ses ayarlarını ve profillerini yönetir.
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

# Ses profilleri - hazır ayarlar
SES_PROFILLERI = {
    "varsayilan": {
        "ad": "Varsayılan Ses",
        "aciklama": "Standart Türkçe ses ayarları",
        "dil": "tr",
        "hiz": 1.0,
        "ses_seviyesi": 1.0,
        "pitch": 1.0,
        "ses_tipi": "gtts",  # gtts, pyttsx3, coqui_tts
        "ses_kalitesi": "normal",  # normal, yuksek, dusuk
        "ses_uzantisi": "mp3",
        "gecici_dosya": True,
        "ses_oynatma": "pydub",  # pydub, playsound, pygame
        "mikrofon_index": 0,
        "mikrofon_enerji_esigi": 4000,
        "mikrofon_dinleme_suresi": 20,
        "mikrofon_gecikme": 0.1,
        "ses_tanima_dili": "tr-TR",
        "ses_tanima_servisi": "google",  # google, sphinx, azure
        "ses_tanima_guven_esigi": 0.7,
        "ses_tanima_timeout": 20,
        "ses_tanima_phrase_time_limit": 10,
        "ses_tanima_ambient_noise_adjustment": True,
        "ses_tanima_dynamic_energy_threshold": True,
        "ses_tanima_pause_threshold": 0.8,
        "ses_tanima_non_speaking_duration": 0.5,
        "ses_tanima_phrase_threshold": 0.3,
        "ses_tanima_max_alternatives": 1,
        "ses_tanima_show_all": False,
        "ses_tanima_with_confidence": False,
        "ses_tanima_word_offsets": False,
        "ses_tanima_profanity_filter": False,
        "ses_tanima_adaptation": None,
        "ses_tanima_audio_config": None,
        "ses_tanima_model": None,
        "ses_tanima_use_enhanced": False,
        "ses_tanima_hints": [],
        "ses_tanima_audio_encoding": None,
        "ses_tanima_sample_rate_hertz": None,
        "ses_tanima_audio_channel_count": None,
        "ses_tanima_enable_automatic_punctuation": False,
        "ses_tanima_enable_word_time_offsets": False,
        "ses_tanima_enable_word_confidence": False,
        "ses_tanima_enable_speaker_diarization": False,
        "ses_tanima_diarization_speaker_count": None,
        "ses_tanima_enable_separate_recognition_per_channel": False,
        "ses_tanima_model": None,
        "ses_tanima_use_enhanced": False,
        "ses_tanima_hints": [],
        "ses_tanima_audio_encoding": None,
        "ses_tanima_sample_rate_hertz": None,
        "ses_tanima_audio_channel_count": None,
        "ses_tanima_enable_automatic_punctuation": False,
        "ses_tanima_enable_word_time_offsets": False,
        "ses_tanima_enable_word_confidence": False,
        "ses_tanima_enable_speaker_diarization": False,
        "ses_tanima_diarization_speaker_count": None,
        "ses_tanima_enable_separate_recognition_per_channel": False
    },
    
    "yavas_ve_net": {
        "ad": "Yavaş ve Net",
        "aciklama": "Daha yavaş ve net konuşma için",
        "dil": "tr",
        "hiz": 0.8,
        "ses_seviyesi": 1.2,
        "pitch": 0.9,
        "ses_tipi": "gtts",
        "ses_kalitesi": "yuksek",
        "ses_uzantisi": "mp3",
        "gecici_dosya": True,
        "ses_oynatma": "pydub",
        "mikrofon_index": 0,
        "mikrofon_enerji_esigi": 3000,
        "mikrofon_dinleme_suresi": 25,
        "mikrofon_gecikme": 0.2,
        "ses_tanima_dili": "tr-TR",
        "ses_tanima_servisi": "google",
        "ses_tanima_guven_esigi": 0.8,
        "ses_tanima_timeout": 25,
        "ses_tanima_phrase_time_limit": 15,
        "ses_tanima_ambient_noise_adjustment": True,
        "ses_tanima_dynamic_energy_threshold": True,
        "ses_tanima_pause_threshold": 1.0,
        "ses_tanima_non_speaking_duration": 0.8,
        "ses_tanima_phrase_threshold": 0.4
    },
    
    "hizli_ve_kompakt": {
        "ad": "Hızlı ve Kompakt",
        "aciklama": "Hızlı ve kısa yanıtlar için",
        "dil": "tr",
        "hiz": 1.3,
        "ses_seviyesi": 0.9,
        "pitch": 1.1,
        "ses_tipi": "gtts",
        "ses_kalitesi": "normal",
        "ses_uzantisi": "mp3",
        "gecici_dosya": True,
        "ses_oynatma": "pydub",
        "mikrofon_index": 0,
        "mikrofon_enerji_esigi": 5000,
        "mikrofon_dinleme_suresi": 15,
        "mikrofon_gecikme": 0.05,
        "ses_tanima_dili": "tr-TR",
        "ses_tanima_servisi": "google",
        "ses_tanima_guven_esigi": 0.6,
        "ses_tanima_timeout": 15,
        "ses_tanima_phrase_time_limit": 8,
        "ses_tanima_ambient_noise_adjustment": False,
        "ses_tanima_dynamic_energy_threshold": False,
        "ses_tanima_pause_threshold": 0.6,
        "ses_tanima_non_speaking_duration": 0.3,
        "ses_tanima_phrase_threshold": 0.2
    },
    
    "profesyonel": {
        "ad": "Profesyonel",
        "aciklama": "Kurumsal çağrı merkezi için",
        "dil": "tr",
        "hiz": 1.0,
        "ses_seviyesi": 1.1,
        "pitch": 1.0,
        "ses_tipi": "gtts",
        "ses_kalitesi": "yuksek",
        "ses_uzantisi": "mp3",
        "gecici_dosya": True,
        "ses_oynatma": "pydub",
        "mikrofon_index": 0,
        "mikrofon_enerji_esigi": 3500,
        "mikrofon_dinleme_suresi": 22,
        "mikrofon_gecikme": 0.15,
        "ses_tanima_dili": "tr-TR",
        "ses_tanima_servisi": "google",
        "ses_tanima_guven_esigi": 0.75,
        "ses_tanima_timeout": 22,
        "ses_tanima_phrase_time_limit": 12,
        "ses_tanima_ambient_noise_adjustment": True,
        "ses_tanima_dynamic_energy_threshold": True,
        "ses_tanima_pause_threshold": 0.9,
        "ses_tanima_non_speaking_duration": 0.6,
        "ses_tanima_phrase_threshold": 0.35
    },
    
    "engelli_dostu": {
        "ad": "Engelli Dostu",
        "aciklama": "İşitme engelli kullanıcılar için",
        "dil": "tr",
        "hiz": 0.7,
        "ses_seviyesi": 1.5,
        "pitch": 0.8,
        "ses_tipi": "gtts",
        "ses_kalitesi": "yuksek",
        "ses_uzantisi": "mp3",
        "gecici_dosya": True,
        "ses_oynatma": "pydub",
        "mikrofon_index": 0,
        "mikrofon_enerji_esigi": 2000,
        "mikrofon_dinleme_suresi": 30,
        "mikrofon_gecikme": 0.3,
        "ses_tanima_dili": "tr-TR",
        "ses_tanima_servisi": "google",
        "ses_tanima_guven_esigi": 0.9,
        "ses_tanima_timeout": 30,
        "ses_tanima_phrase_time_limit": 20,
        "ses_tanima_ambient_noise_adjustment": True,
        "ses_tanima_dynamic_energy_threshold": True,
        "ses_tanima_pause_threshold": 1.2,
        "ses_tanima_non_speaking_duration": 1.0,
        "ses_tanima_phrase_threshold": 0.5
    },
    
    "gurultulu_ortam": {
        "ad": "Gürültülü Ortam",
        "aciklama": "Gürültülü ortamlarda kullanım için",
        "dil": "tr",
        "hiz": 1.0,
        "ses_seviyesi": 1.3,
        "pitch": 1.0,
        "ses_tipi": "gtts",
        "ses_kalitesi": "yuksek",
        "ses_uzantisi": "mp3",
        "gecici_dosya": True,
        "ses_oynatma": "pydub",
        "mikrofon_index": 0,
        "mikrofon_enerji_esigi": 6000,
        "mikrofon_dinleme_suresi": 18,
        "mikrofon_gecikme": 0.08,
        "ses_tanima_dili": "tr-TR",
        "ses_tanima_servisi": "google",
        "ses_tanima_guven_esigi": 0.5,
        "ses_tanima_timeout": 18,
        "ses_tanima_phrase_time_limit": 10,
        "ses_tanima_ambient_noise_adjustment": True,
        "ses_tanima_dynamic_energy_threshold": True,
        "ses_tanima_pause_threshold": 0.7,
        "ses_tanima_non_speaking_duration": 0.4,
        "ses_tanima_phrase_threshold": 0.25
    }
}

class SesYoneticisi:
    """Ses ayarlarını yöneten sınıf"""
    
    def __init__(self, profil_adi: str = "varsayilan"):
        self.aktif_profil = self.profil_yukle(profil_adi)
        self.gecici_dosyalar = []
    
    def profil_yukle(self, profil_adi: str) -> Dict[str, Any]:
        """Belirtilen profili yükler"""
        if profil_adi in SES_PROFILLERI:
            return SES_PROFILLERI[profil_adi].copy()
        else:
            print(f"Uyarı: '{profil_adi}' profili bulunamadı. Varsayılan profil kullanılıyor.")
            return SES_PROFILLERI["varsayilan"].copy()
    
    def profil_degistir(self, profil_adi: str) -> bool:
        """Aktif profili değiştirir"""
        if profil_adi in SES_PROFILLERI:
            self.aktif_profil = self.profil_yukle(profil_adi)
            print(f"Ses profili '{profil_adi}' olarak değiştirildi.")
            return True
        else:
            print(f"Hata: '{profil_adi}' profili bulunamadı.")
            return False
    
    def ayar_guncelle(self, ayar_adi: str, yeni_deger: Any) -> bool:
        """Belirli bir ayarı günceller"""
        if ayar_adi in self.aktif_profil:
            self.aktif_profil[ayar_adi] = yeni_deger
            print(f"Ayar '{ayar_adi}' güncellendi: {yeni_deger}")
            return True
        else:
            print(f"Hata: '{ayar_adi}' ayarı bulunamadı.")
            return False
    
    def profil_olustur(self, profil_adi: str, ayarlar: Dict[str, Any]) -> bool:
        """Yeni profil oluşturur"""
        if profil_adi in SES_PROFILLERI:
            print(f"Hata: '{profil_adi}' profili zaten mevcut.")
            return False
        
        # Varsayılan ayarları temel al
        yeni_profil = SES_PROFILLERI["varsayilan"].copy()
        yeni_profil.update(ayarlar)
        yeni_profil["ad"] = profil_adi
        yeni_profil["aciklama"] = ayarlar.get("aciklama", "Özel profil")
        
        SES_PROFILLERI[profil_adi] = yeni_profil
        print(f"Yeni profil '{profil_adi}' oluşturuldu.")
        return True
    
    def profil_sil(self, profil_adi: str) -> bool:
        """Profil siler"""
        if profil_adi == "varsayilan":
            print("Hata: Varsayılan profil silinemez.")
            return False
        
        if profil_adi in SES_PROFILLERI:
            del SES_PROFILLERI[profil_adi]
            print(f"Profil '{profil_adi}' silindi.")
            return True
        else:
            print(f"Hata: '{profil_adi}' profili bulunamadı.")
            return False
    
    def profil_listele(self) -> Dict[str, str]:
        """Mevcut profilleri listeler"""
        return {adi: profil["ad"] for adi, profil in SES_PROFILLERI.items()}
    
    def profil_bilgisi(self, profil_adi: str = None) -> Dict[str, Any]:
        """Profil bilgilerini döndürür"""
        if profil_adi is None:
            profil_adi = list(self.aktif_profil.keys())[0]
        
        if profil_adi in SES_PROFILLERI:
            return SES_PROFILLERI[profil_adi]
        else:
            return {}
    
    def gecici_dosya_olustur(self) -> str:
        """Geçici ses dosyası oluşturur"""
        if self.aktif_profil.get("gecici_dosya", True):
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=f'.{self.aktif_profil.get("ses_uzantisi", "mp3")}'
            )
            self.gecici_dosyalar.append(temp_file.name)
            return temp_file.name
        else:
            # Kalıcı dosya için
            return f"ses_{len(self.gecici_dosyalar)}.{self.aktif_profil.get('ses_uzantisi', 'mp3')}"
    
    def gecici_dosyalari_temizle(self):
        """Geçici dosyaları temizler"""
        for dosya in self.gecici_dosyalar:
            try:
                if os.path.exists(dosya):
                    os.remove(dosya)
            except Exception as e:
                print(f"Geçici dosya silinemedi: {e}")
        self.gecici_dosyalar.clear()

# Global ses yöneticisi örneği
ses_yoneticisi = SesYoneticisi()

def ses_profili_degistir(profil_adi: str) -> bool:
    """Global ses profilini değiştirir"""
    return ses_yoneticisi.profil_degistir(profil_adi)

def ses_ayari_guncelle(ayar_adi: str, yeni_deger: Any) -> bool:
    """Global ses ayarını günceller"""
    return ses_yoneticisi.ayar_guncelle(ayar_adi, yeni_deger)

def mevcut_profilleri_listele() -> Dict[str, str]:
    """Mevcut profilleri listeler"""
    return ses_yoneticisi.profil_listele()

def aktif_profil_bilgisi() -> Dict[str, Any]:
    """Aktif profil bilgilerini döndürür"""
    return ses_yoneticisi.aktif_profil

# Kullanım örnekleri:
if __name__ == "__main__":
    # Profilleri listele
    print("Mevcut profiller:")
    for anahtar, ad in mevcut_profilleri_listele().items():
        print(f"  {anahtar}: {ad}")
    
    # Profil değiştir
    ses_profili_degistir("yavas_ve_net")
    
    # Ayar güncelle
    ses_ayari_guncelle("hiz", 0.9)
    
    # Aktif profil bilgisi
    print("\nAktif profil:")
    for anahtar, deger in aktif_profil_bilgisi().items():
        print(f"  {anahtar}: {deger}")
