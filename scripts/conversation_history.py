#!/usr/bin/env python3
"""
Conversation History System - Advanced Call Records and Customer Analytics
This module provides detailed call recording and customer analysis capabilities.

Developed by Trivox Team:
- Serhatcan Ünal, Elif Zeynep Tosun, Meryem Gençali, Ali Buğrahan Budak

Features:
- Comprehensive conversation logging
- Customer interaction history
- Statistical analysis and reporting
- Search and filtering capabilities
- Performance metrics tracking

Gelişmiş Geçmiş Görüşmeler Sistemi
Detaylı çağrı kayıtları ve müşteri analizi sağlar.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import uuid
from typing import Dict, List, Optional, Any

class GelismisGecmisGorusmeler:
    def __init__(self, data_file: str = "data/conversation_history.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.gorusmeler = self._load_data()
        self._istatistikleri_guncelle()
    
    def _load_data(self) -> Dict:
        """Veri dosyasını yükle"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Geçmiş görüşmeler yüklenirken hata: {e}")
                return {"gorusmeler": [], "musteri_gecmis": {}, "kategori_istatistikleri": {}}
        return {"gorusmeler": [], "musteri_gecmis": {}, "kategori_istatistikleri": {}}
    
    def _save_data(self):
        """Veriyi dosyaya kaydet"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.gorusmeler, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Geçmiş görüşmeler kaydedilirken hata: {e}")
    
    def yeni_gorusme_baslat(self, telefon: str, musteri_adi: str, kategori: Optional[str] = None) -> str:
        """Yeni görüşme başlat"""
        gorusme_id = str(uuid.uuid4())
        baslangic_zamani = datetime.now()
        
        yeni_gorusme = {
            "id": gorusme_id,
            "telefon": telefon,
            "musteri_adi": musteri_adi,
            "baslangic_zamani": baslangic_zamani.isoformat(),
            "bitis_zamani": None,
            "sure": 0,
            "durum": "aktif",
            "kategori": kategori,
            "mesajlar": [],
            "kategori_gecmisi": [],

            "cozulme_durumu": "devam_ediyor",
            "oncelik": "normal",
            "etiketler": [],
            "notlar": ""
        }
        
        self.gorusmeler["gorusmeler"].append(yeni_gorusme)
        
        # Müşteri geçmişini güncelle
        if telefon not in self.gorusmeler["musteri_gecmis"]:
            self.gorusmeler["musteri_gecmis"][telefon] = {
                "musteri_adi": musteri_adi,
                "ilk_gorusme": baslangic_zamani.isoformat(),
                "son_gorusme": baslangic_zamani.isoformat(),
                "toplam_gorusme": 0,
                "toplam_sure": 0,
                "kategoriler": {},
                "sorun_gecmisi": [],


            }
        
        musteri_data = self.gorusmeler["musteri_gecmis"][telefon]
        musteri_data["toplam_gorusme"] += 1
        musteri_data["son_gorusme"] = baslangic_zamani.isoformat()
        
        self._save_data()
        return gorusme_id
    
    def gorusme_bitir(self, gorusme_id: str, durum: str = "tamamlandi", cozulme_durumu: str = "cozuldu"):
        """Görüşmeyi bitir"""
        for gorusme in self.gorusmeler["gorusmeler"]:
            if gorusme["id"] == gorusme_id:
                bitis_zamani = datetime.now()
                baslangic = datetime.fromisoformat(gorusme["baslangic_zamani"])
                sure = (bitis_zamani - baslangic).total_seconds() / 60  # dakika
                
                gorusme["bitis_zamani"] = bitis_zamani.isoformat()
                gorusme["sure"] = round(sure, 2)
                gorusme["durum"] = durum

                gorusme["cozulme_durumu"] = cozulme_durumu
                
                # Müşteri geçmişini güncelle
                telefon = gorusme["telefon"]
                if telefon in self.gorusmeler["musteri_gecmis"]:
                    musteri_data = self.gorusmeler["musteri_gecmis"][telefon]
                    musteri_data["toplam_sure"] += sure
                    
                    # Kategori istatistiklerini güncelle
                    if gorusme["kategori"]:
                        if gorusme["kategori"] not in musteri_data["kategoriler"]:
                            musteri_data["kategoriler"][gorusme["kategori"]] = 0
                        musteri_data["kategoriler"][gorusme["kategori"]] += 1
                    

                    
                break
        
        self._istatistikleri_guncelle()
        self._save_data()
    
    def mesaj_ekle(self, gorusme_id: str, gonderen: str, mesaj: str, kategori: Optional[str] = None):
        """Mesaj ekle"""
        for gorusme in self.gorusmeler["gorusmeler"]:
            if gorusme["id"] == gorusme_id:
                mesaj_data = {
                    "zaman": datetime.now().isoformat(),
                    "gonderen": gonderen,
                    "mesaj": mesaj,
                    "kategori": kategori
                }
                gorusme["mesajlar"].append(mesaj_data)
                
                # Kategori geçmişini güncelle
                if kategori and kategori not in gorusme["kategori_gecmisi"]:
                    gorusme["kategori_gecmisi"].append(kategori)
                
                break
        
        self._save_data()
    
    def kategori_guncelle(self, gorusme_id: str, kategori: str):
        """Görüşme kategorisini güncelle"""
        for gorusme in self.gorusmeler["gorusmeler"]:
            if gorusme["id"] == gorusme_id:
                gorusme["kategori"] = kategori
                if kategori not in gorusme["kategori_gecmisi"]:
                    gorusme["kategori_gecmisi"].append(kategori)
                break
        
        self._save_data()
    
    def musteri_gecmis_getir(self, telefon: str) -> Optional[Dict]:
        """Müşteri geçmişini getir"""
        return self.gorusmeler["musteri_gecmis"].get(telefon)
    
    def musteri_gorusmeleri_getir(self, telefon: str, limit: int = 10) -> List[Dict]:
        """Müşterinin geçmiş görüşmelerini getir"""
        musteri_gorusmeleri = [g for g in self.gorusmeler["gorusmeler"] if g["telefon"] == telefon]
        musteri_gorusmeleri.sort(key=lambda x: x["baslangic_zamani"], reverse=True)
        return musteri_gorusmeleri[:limit]
    
    def musteri_kategori_analizi(self, telefon: str) -> Dict:
        """Müşteri kategori analizi"""
        musteri_gorusmeleri = [g for g in self.gorusmeler["gorusmeler"] if g["telefon"] == telefon]
        
        kategori_sayilari = {}
        kategori_sureleri = {}
        
        for gorusme in musteri_gorusmeleri:
            kategori = gorusme.get("kategori", "Bilinmiyor")
            sure = gorusme.get("sure", 0)
            
            if kategori not in kategori_sayilari:
                kategori_sayilari[kategori] = 0
                kategori_sureleri[kategori] = 0
            
            kategori_sayilari[kategori] += 1
            kategori_sureleri[kategori] += sure
        
        return {
            "kategori_sayilari": kategori_sayilari,
            "kategori_sureleri": kategori_sureleri,
            "en_cok_gorusulen_kategori": max(kategori_sayilari.items(), key=lambda x: x[1])[0] if kategori_sayilari else "Yok",
            "toplam_gorusme": len(musteri_gorusmeleri)
        }
    
    def _istatistikleri_guncelle(self):
        """Genel istatistikleri güncelle"""
        gorusmeler = self.gorusmeler["gorusmeler"]
        
        # Kategori istatistikleri
        kategori_sayilari = {}
        kategori_sureleri = {}
        
        for gorusme in gorusmeler:
            kategori = gorusme.get("kategori", "Bilinmiyor")
            sure = gorusme.get("sure", 0)
            
            if kategori not in kategori_sayilari:
                kategori_sayilari[kategori] = 0
                kategori_sureleri[kategori] = 0
            
            kategori_sayilari[kategori] += 1
            kategori_sureleri[kategori] += sure
        
        self.gorusmeler["kategori_istatistikleri"] = {
            "kategori_sayilari": kategori_sayilari,
            "kategori_sureleri": kategori_sureleri,
            "toplam_gorusme": len(gorusmeler),
            "aktif_gorusme": len([g for g in gorusmeler if g["durum"] == "aktif"]),
            "tamamlanan_gorusme": len([g for g in gorusmeler if g["durum"] == "tamamlandi"]),

        }
    
    def istatistikleri_getir(self) -> Dict:
        """Genel istatistikleri getir"""
        self._istatistikleri_guncelle()
        return self.gorusmeler["kategori_istatistikleri"]
    
    def son_gorusmeler_getir(self, limit: int = 20) -> List[Dict]:
        """Son görüşmeleri getir"""
        gorusmeler = sorted(self.gorusmeler["gorusmeler"], 
                           key=lambda x: x["baslangic_zamani"], reverse=True)
        return gorusmeler[:limit]
    
    def gorusme_ara(self, arama_terimi: str) -> List[Dict]:
        """Görüşme ara"""
        sonuclar = []
        arama_terimi = arama_terimi.lower()
        
        for gorusme in self.gorusmeler["gorusmeler"]:
            # Müşteri adı, telefon, kategori veya mesajlarda ara
            kategori = gorusme.get("kategori", "")
            kategori_str = str(kategori).lower() if kategori else ""
            
            if (arama_terimi in gorusme["musteri_adi"].lower() or
                arama_terimi in gorusme["telefon"] or
                arama_terimi in kategori_str or
                any(arama_terimi in mesaj["mesaj"].lower() for mesaj in gorusme["mesajlar"])):
                sonuclar.append(gorusme)
        
        return sonuclar
    
    def gorusme_sil(self, gorusme_id: str) -> bool:
        """Görüşme sil"""
        for i, gorusme in enumerate(self.gorusmeler["gorusmeler"]):
            if gorusme["id"] == gorusme_id:
                del self.gorusmeler["gorusmeler"][i]
                self._istatistikleri_guncelle()
                self._save_data()
                return True
        return False
    
    def gorusme_guncelle(self, gorusme_id: str, **kwargs) -> bool:
        """Görüşme güncelle"""
        for gorusme in self.gorusmeler["gorusmeler"]:
            if gorusme["id"] == gorusme_id:
                gorusme.update(kwargs)
                self._save_data()
                return True
        return False
    
    def gunluk_istatistikler(self) -> Dict:
        """Günlük istatistikler"""
        bugun = datetime.now().date()
        bugun_gorusmeleri = []
        
        for gorusme in self.gorusmeler["gorusmeler"]:
            gorusme_tarihi = datetime.fromisoformat(gorusme["baslangic_zamani"]).date()
            if gorusme_tarihi == bugun:
                bugun_gorusmeleri.append(gorusme)
        
        return {
            "bugun_gorusme": len(bugun_gorusmeleri),
            "bugun_sure": sum(g.get("sure", 0) for g in bugun_gorusmeleri),
            "bugun_kategoriler": {},
            "bugun_cozulme": len([g for g in bugun_gorusmeleri if g["cozulme_durumu"] == "cozuldu"])
        }
    
    def musteri_analizi(self, telefon: str) -> Dict:
        """Detaylı müşteri analizi"""
        musteri_gorusmeleri = [g for g in self.gorusmeler["gorusmeler"] if g["telefon"] == telefon]
        
        if not musteri_gorusmeleri:
            return {}
        
        # Zaman analizi
        son_gorusme = max(musteri_gorusmeleri, key=lambda x: x["baslangic_zamani"])
        ilk_gorusme = min(musteri_gorusmeleri, key=lambda x: x["baslangic_zamani"])
        
        son_gorusme_tarihi = datetime.fromisoformat(son_gorusme["baslangic_zamani"])
        ilk_gorusme_tarihi = datetime.fromisoformat(ilk_gorusme["baslangic_zamani"])
        
        # Kategori analizi
        kategori_analizi = self.musteri_kategori_analizi(telefon)
        
        
        return {
            "toplam_gorusme": len(musteri_gorusmeleri),
            "ilk_gorusme": ilk_gorusme_tarihi.isoformat(),
            "son_gorusme": son_gorusme_tarihi.isoformat(),
            "musteri_yasi_gun": (datetime.now() - ilk_gorusme_tarihi).days,
            "ortalama_gorusme_suresi": sum(g.get("sure", 0) for g in musteri_gorusmeleri) / len(musteri_gorusmeleri),
            "toplam_gorusme_suresi": sum(g.get("sure", 0) for g in musteri_gorusmeleri),
            "kategori_analizi": kategori_analizi,


            "son_30_gun_gorusme": len([g for g in musteri_gorusmeleri 
                                      if (datetime.now() - datetime.fromisoformat(g["baslangic_zamani"])).days <= 30])
        }

# Global instance
gecmis_yoneticisi = GelismisGecmisGorusmeler()
