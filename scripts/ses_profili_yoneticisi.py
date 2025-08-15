#!/usr/bin/env python3
"""
Ses Profili Yöneticisi
Bu script ses profillerini yönetmek için kullanılır.
"""

import sys
import os
from pathlib import Path

# Scripts dizinini Python path'ine ekle
current_file = Path(__file__).resolve()
scripts_dir = current_file.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

try:
    from voice_config import (
        ses_yoneticisi, 
        ses_profili_degistir, 
        ses_ayari_guncelle, 
        mevcut_profilleri_listele, 
        aktif_profil_bilgisi
    )
except ImportError:
    print("❌ voice_config.py dosyası bulunamadı!")
    print("Lütfen scripts/ dizininde voice_config.py dosyasının olduğundan emin olun.")
    sys.exit(1)

def profil_listele():
    """Mevcut profilleri listeler"""
    print("\n🎵 Mevcut Ses Profilleri:")
    print("=" * 50)
    
    profiller = mevcut_profilleri_listele()
    aktif_profil = aktif_profil_bilgisi()
    
    for anahtar, ad in profiller.items():
        if anahtar in aktif_profil:
            print(f"  ✅ {anahtar}: {ad} (AKTİF)")
        else:
            print(f"     {anahtar}: {ad}")
    
    print(f"\n📋 Toplam {len(profiller)} profil mevcut.")

def profil_detay(profil_adi):
    """Profil detaylarını gösterir"""
    if profil_adi in mevcut_profilleri_listele():
        profil = ses_yoneticisi.profil_bilgisi(profil_adi)
        print(f"\n📊 {profil['ad']} Profili Detayları:")
        print("=" * 50)
        print(f"📝 Açıklama: {profil.get('aciklama', 'Açıklama yok')}")
        print(f"🌍 Dil: {profil.get('dil', 'tr')}")
        print(f"⚡ Hız: {profil.get('hiz', 1.0)}")
        print(f"🔊 Ses Seviyesi: {profil.get('ses_seviyesi', 1.0)}")
        print(f"🎵 Pitch: {profil.get('pitch', 1.0)}")
        print(f"🎤 Ses Tipi: {profil.get('ses_tipi', 'gtts')}")
        print(f"🎧 Ses Kalitesi: {profil.get('ses_kalitesi', 'normal')}")
        print(f"🎬 Ses Oynatma: {profil.get('ses_oynatma', 'pydub')}")
        print(f"🎤 Mikrofon Index: {profil.get('mikrofon_index', 0)}")
        print(f"🔊 Mikrofon Enerji Eşiği: {profil.get('mikrofon_enerji_esigi', 4000)}")
        print(f"⏱️ Dinleme Süresi: {profil.get('mikrofon_dinleme_suresi', 20)} saniye")
        print(f"🎯 Ses Tanıma Dili: {profil.get('ses_tanima_dili', 'tr-TR')}")
        print(f"🎯 Ses Tanıma Güven Eşiği: {profil.get('ses_tanima_guven_esigi', 0.7)}")
    else:
        print(f"❌ '{profil_adi}' profili bulunamadı!")

def profil_degistir(profil_adi):
    """Profil değiştirir"""
    if ses_profili_degistir(profil_adi):
        print(f"✅ Ses profili '{profil_adi}' olarak değiştirildi.")
        profil_detay(profil_adi)
    else:
        print(f"❌ Profil değiştirilemedi!")

def ayar_guncelle(ayar_adi, yeni_deger):
    """Belirli bir ayarı günceller"""
    try:
        # Sayısal değerleri dönüştür
        if yeni_deger.lower() in ['true', 'evet', 'yes', '1']:
            yeni_deger = True
        elif yeni_deger.lower() in ['false', 'hayir', 'no', '0']:
            yeni_deger = False
        elif yeni_deger.replace('.', '').replace('-', '').isdigit():
            if '.' in yeni_deger:
                yeni_deger = float(yeni_deger)
            else:
                yeni_deger = int(yeni_deger)
        
        if ses_ayari_guncelle(ayar_adi, yeni_deger):
            print(f"✅ Ayar '{ayar_adi}' güncellendi: {yeni_deger}")
        else:
            print(f"❌ Ayar güncellenemedi!")
    except ValueError:
        print(f"❌ Geçersiz değer: {yeni_deger}")

def test_ses():
    """Ses testi yapar"""
    print("\n🎵 Ses Testi Başlatılıyor...")
    print("Bu test mevcut ses ayarlarınızı kontrol edecek.")
    
    try:
        # Test metni
        test_metni = "Merhaba, bu bir ses testidir. Ses ayarlarınız çalışıyor."
        
        # Ses yöneticisini kullanarak test
        if ses_yoneticisi:
            print("🔊 Ses üretiliyor...")
            
            # Geçici dosya oluştur
            mp3_dosyasi = ses_yoneticisi.gecici_dosya_olustur()
            
            # gTTS ile ses üret
            from gtts import gTTS
            dil = ses_yoneticisi.aktif_profil.get("dil", "tr")
            hiz = ses_yoneticisi.aktif_profil.get("hiz", 1.0)
            
            tts = gTTS(text=test_metni, lang=dil, slow=(hiz < 0.8))
            tts.save(mp3_dosyasi)
            
            print("🎵 Ses oynatılıyor...")
            
            # Ses oynat
            ses_oynatma = ses_yoneticisi.aktif_profil.get("ses_oynatma", "pydub")
            if ses_oynatma == "pydub":
                from pydub import AudioSegment
                from pydub.playback import play
                sound = AudioSegment.from_mp3(mp3_dosyasi)
                play(sound)
            else:
                from playsound import playsound
                playsound(mp3_dosyasi)
            
            print("✅ Ses testi tamamlandı!")
            
            # Geçici dosyaları temizle
            ses_yoneticisi.gecici_dosyalari_temizle()
        else:
            print("❌ Ses yöneticisi bulunamadı!")
            
    except Exception as e:
        print(f"❌ Ses testi başarısız: {e}")

def yardim():
    """Yardım menüsünü gösterir"""
    print("\n🎵 Ses Profili Yöneticisi - Yardım")
    print("=" * 50)
    print("Kullanım: python ses_profili_yoneticisi.py [komut] [parametreler]")
    print("\nKomutlar:")
    print("  listele                    - Mevcut profilleri listeler")
    print("  detay <profil_adi>         - Profil detaylarını gösterir")
    print("  degistir <profil_adi>      - Aktif profili değiştirir")
    print("  ayar <ayar_adi> <deger>    - Belirli bir ayarı günceller")
    print("  test                       - Ses testi yapar")
    print("  yardim                     - Bu yardım menüsünü gösterir")
    print("\nÖrnekler:")
    print("  python ses_profili_yoneticisi.py listele")
    print("  python ses_profili_yoneticisi.py degistir yavas_ve_net")
    print("  python ses_profili_yoneticisi.py ayar hiz 0.8")
    print("  python ses_profili_yoneticisi.py detay profesyonel")
    print("  python ses_profili_yoneticisi.py test")

def main():
    """Ana fonksiyon"""
    print("🎵 Çağrı Merkezi Ses Profili Yöneticisi")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("❌ Komut belirtilmedi!")
        yardim()
        return
    
    komut = sys.argv[1].lower()
    
    if komut == "listele":
        profil_listele()
    
    elif komut == "detay":
        if len(sys.argv) < 3:
            print("❌ Profil adı belirtilmedi!")
            return
        profil_detay(sys.argv[2])
    
    elif komut == "degistir":
        if len(sys.argv) < 3:
            print("❌ Profil adı belirtilmedi!")
            return
        profil_degistir(sys.argv[2])
    
    elif komut == "ayar":
        if len(sys.argv) < 4:
            print("❌ Ayar adı ve değeri belirtilmedi!")
            return
        ayar_guncelle(sys.argv[2], sys.argv[3])
    
    elif komut == "test":
        test_ses()
    
    elif komut == "yardim":
        yardim()
    
    else:
        print(f"❌ Bilinmeyen komut: {komut}")
        yardim()

if __name__ == "__main__":
    main()
