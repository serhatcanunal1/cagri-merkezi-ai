"""
Müşteri Bilgileri Popup Penceresi
Bu modül müşteri kimliği doğrulandığında popup ile müşteri bilgilerini gösterir.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Geçmiş görüşmeler modülünü import et
try:
    from conversation_history import gecmis_yoneticisi
except ImportError:
    print("Uyarı: conversation_history.py bulunamadı. Geçmiş görüşmeler özelliği devre dışı.")
    gecmis_yoneticisi = None

class MusteriPopup:
    """Müşteri bilgilerini gösteren popup penceresi"""
    
    def __init__(self, parent, musteri_verisi: Dict[str, Any]):
        self.parent = parent
        self.musteri_verisi = musteri_verisi
        
        # Popup penceresi oluştur
        self.popup = tk.Toplevel(parent)
        self.popup.title("Müşteri Bilgileri")
        self.popup.geometry("600x700")
        self.popup.resizable(True, True)
        
        # Pencereyi merkeze konumlandır
        self.popup.transient(parent)
        self.popup.grab_set()
        
        # Pencere ikonu (varsa)
        try:
            self.popup.iconbitmap("icon.ico")
        except:
            pass
        
        # Ana frame
        self.main_frame = ttk.Frame(self.popup, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid ağırlıkları
        self.popup.columnconfigure(0, weight=1)
        self.popup.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        self._create_widgets()
        self._load_musteri_data()
        
        # Pencereyi odakla
        self.popup.focus_set()
        self.popup.wait_window()
    
    def _create_widgets(self):
        """Widget'ları oluştur"""
        
        # Başlık
        title_label = ttk.Label(
            self.main_frame, 
            text="🎯 Müşteri Bilgileri", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Temel Bilgiler Bölümü
        self._create_basic_info_section()
        
        # Paket Bilgileri Bölümü
        self._create_package_info_section()
        
        # Kullanım Bilgileri Bölümü
        self._create_usage_info_section()
        
        # Fatura Bilgileri Bölümü
        self._create_billing_info_section()
        
        # Butonlar
        self._create_buttons()
    
    def _create_basic_info_section(self):
        """Temel bilgiler bölümünü oluştur"""
        # Bölüm başlığı
        basic_title = ttk.Label(
            self.main_frame, 
            text="👤 Temel Bilgiler", 
            font=("Arial", 12, "bold")
        )
        basic_title.grid(row=1, column=0, columnspan=2, pady=(10, 5), sticky=tk.W)
        
        # Bilgi alanları
        row = 2
        self.basic_labels = {}
        
        basic_fields = [
            ("Ad Soyad:", "ad"),
            ("Telefon:", "numara"),
            ("TC Kimlik:", "tc"),
            ("E-posta:", "email"),
            ("Adres:", "adres")
        ]
        
        for label_text, field_name in basic_fields:
            ttk.Label(self.main_frame, text=label_text, font=("Arial", 10, "bold")).grid(
                row=row, column=0, sticky=tk.W, padx=(0, 10), pady=2
            )
            
            value_label = ttk.Label(self.main_frame, text="", font=("Arial", 10))
            value_label.grid(row=row, column=1, sticky=tk.W, pady=2)
            
            self.basic_labels[field_name] = value_label
            row += 1
    
    def _create_package_info_section(self):
        """Paket bilgileri bölümünü oluştur"""
        # Bölüm başlığı
        package_title = ttk.Label(
            self.main_frame, 
            text="📦 Paket Bilgileri", 
            font=("Arial", 12, "bold")
        )
        package_title.grid(row=7, column=0, columnspan=2, pady=(15, 5), sticky=tk.W)
        
        # Paket bilgileri
        row = 8
        self.package_labels = {}
        
        package_fields = [
            ("Paket Adı:", "paket_adi"),
            ("Paket Fiyatı:", "paket_fiyati"),
            ("Dakika Limiti:", "dakika_limiti"),
            ("SMS Limiti:", "sms_limiti"),
            ("İnternet Limiti:", "internet_limiti"),
            ("Geçerlilik Tarihi:", "gecerlilik_tarihi")
        ]
        
        for label_text, field_name in package_fields:
            ttk.Label(self.main_frame, text=label_text, font=("Arial", 10, "bold")).grid(
                row=row, column=0, sticky=tk.W, padx=(0, 10), pady=2
            )
            
            value_label = ttk.Label(self.main_frame, text="", font=("Arial", 10))
            value_label.grid(row=row, column=1, sticky=tk.W, pady=2)
            
            self.package_labels[field_name] = value_label
            row += 1
    
    def _create_usage_info_section(self):
        """Kullanım bilgileri bölümünü oluştur"""
        # Bölüm başlığı
        usage_title = ttk.Label(
            self.main_frame, 
            text="📊 Kullanım Bilgileri", 
            font=("Arial", 12, "bold")
        )
        usage_title.grid(row=14, column=0, columnspan=2, pady=(15, 5), sticky=tk.W)
        
        # Kalan haklar
        row = 15
        self.usage_labels = {}
        
        usage_fields = [
            ("Kalan Dakika:", "kalan_dakika"),
            ("Kalan SMS:", "kalan_sms"),
            ("Kalan İnternet:", "kalan_internet"),
            ("Son Kullanım Tarihi:", "son_kullanim_tarihi")
        ]
        
        for label_text, field_name in usage_fields:
            ttk.Label(self.main_frame, text=label_text, font=("Arial", 10, "bold")).grid(
                row=row, column=0, sticky=tk.W, padx=(0, 10), pady=2
            )
            
            value_label = ttk.Label(self.main_frame, text="", font=("Arial", 10))
            value_label.grid(row=row, column=1, sticky=tk.W, pady=2)
            
            self.usage_labels[field_name] = value_label
            row += 1
    
    def _create_billing_info_section(self):
        """Fatura bilgileri bölümünü oluştur"""
        # Bölüm başlığı
        billing_title = ttk.Label(
            self.main_frame, 
            text="💰 Fatura Bilgileri", 
            font=("Arial", 12, "bold")
        )
        billing_title.grid(row=19, column=0, columnspan=2, pady=(15, 5), sticky=tk.W)
        
        # Fatura bilgileri
        row = 20
        self.billing_labels = {}
        
        billing_fields = [
            ("Son Fatura Tutarı:", "son_fatura_tutari"),
            ("Son Ödeme Tarihi:", "son_odeme_tarihi"),
            ("Fatura Durumu:", "fatura_durumu"),
            ("Toplam Borç:", "toplam_borc")
        ]
        
        for label_text, field_name in billing_fields:
            ttk.Label(self.main_frame, text=label_text, font=("Arial", 10, "bold")).grid(
                row=row, column=0, sticky=tk.W, padx=(0, 10), pady=2
            )
            
            value_label = ttk.Label(self.main_frame, text="", font=("Arial", 10))
            value_label.grid(row=row, column=1, sticky=tk.W, pady=2)
            
            self.billing_labels[field_name] = value_label
            row += 1
    
    def _create_buttons(self):
        """Butonları oluştur"""
        # Buton frame'i
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=24, column=0, columnspan=2, pady=(20, 0))
        
        # Kapat butonu
        close_btn = ttk.Button(
            button_frame, 
            text="❌ Kapat", 
            command=self.popup.destroy,
            style="Accent.TButton"
        )
        close_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Detaylı Görüntüle butonu
        detail_btn = ttk.Button(
            button_frame, 
            text="📋 Detaylı Görüntüle", 
            command=self._show_detailed_view
        )
        detail_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Düzenle butonu
        edit_btn = ttk.Button(
            button_frame, 
            text="✏️ Düzenle", 
            command=self._edit_customer
        )
        edit_btn.pack(side=tk.LEFT)
    
    def _load_musteri_data(self):
        """Müşteri verilerini yükle ve göster"""
        try:
            # Temel bilgiler
            self.basic_labels["ad"].config(text=self.musteri_verisi.get("ad", "Belirtilmemiş"))
            self.basic_labels["numara"].config(text=self.musteri_verisi.get("numara", "Belirtilmemiş"))
            self.basic_labels["tc"].config(text=self.musteri_verisi.get("tc", "Belirtilmemiş"))
            self.basic_labels["email"].config(text=self.musteri_verisi.get("email", "Belirtilmemiş"))
            self.basic_labels["adres"].config(text=self.musteri_verisi.get("adres", "Belirtilmemiş"))
            
            # Paket bilgileri
            paket = self.musteri_verisi.get("numaraya_tanimli_paket", {})
            self.package_labels["paket_adi"].config(text=paket.get("paketİsmi", "Belirtilmemiş"))
            self.package_labels["paket_fiyati"].config(text=f"{paket.get('fiyatı', 0)} TL")
            self.package_labels["dakika_limiti"].config(text=f"{paket.get('dakika', 0)} dakika")
            self.package_labels["sms_limiti"].config(text=f"{paket.get('sms', 0)} SMS")
            
            # İnternet limiti (MB/GB dönüşümü)
            data_gb = paket.get("data_gb", 0)
            if data_gb >= 1024:
                internet_text = f"{data_gb/1024:.1f} GB"
            else:
                internet_text = f"{data_gb} MB"
            self.package_labels["internet_limiti"].config(text=internet_text)
            
            self.package_labels["gecerlilik_tarihi"].config(
                text=paket.get("gecerlilikTarihi", "Belirtilmemiş")
            )
            
            # Kullanım bilgileri
            kalanlar = self.musteri_verisi.get("kalan_kullanim_haklari", {})
            self.usage_labels["kalan_dakika"].config(text=f"{kalanlar.get('kalanDakika', 0)} dakika")
            self.usage_labels["kalan_sms"].config(text=f"{kalanlar.get('kalanSms', 0)} SMS")
            self.usage_labels["kalan_internet"].config(text=f"{kalanlar.get('kalanİnternet', 0)} GB")
            self.usage_labels["son_kullanim_tarihi"].config(
                text=kalanlar.get("sonKullanimTarihi", "Belirtilmemiş")
            )
            
            # Fatura bilgileri
            son_4_ay = self.musteri_verisi.get("son_4_aylik_kullanim", [])
            if son_4_ay:
                son_ay = son_4_ay[-1]
                self.billing_labels["son_fatura_tutari"].config(
                    text=f"{son_ay.get('odeme_tl', 0)} TL"
                )
            
            self.billing_labels["son_odeme_tarihi"].config(
                text=self.musteri_verisi.get("son_odeme_tarihi", "Belirtilmemiş")
            )
            
            # Fatura durumu
            fatura_odendi = self.musteri_verisi.get("fatura_odendi_mi", None)
            if fatura_odendi is True:
                durum_text = "✅ Ödendi"
                durum_color = "green"
            elif fatura_odendi is False:
                durum_text = "❌ Ödenmedi"
                durum_color = "red"
            else:
                durum_text = "❓ Belirsiz"
                durum_color = "orange"
            
            self.billing_labels["fatura_durumu"].config(text=durum_text, foreground=durum_color)
            
            # Toplam borç hesaplama
            toplam_borc = 0
            for ay in son_4_ay:
                if not ay.get("odendi_mi", True):
                    toplam_borc += ay.get("odeme_tl", 0)
            
            self.billing_labels["toplam_borc"].config(text=f"{toplam_borc} TL")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Müşteri verileri yüklenirken hata oluştu: {e}")
    
    def _show_detailed_view(self):
        """Detaylı görünüm penceresi"""
        try:
            detailed_popup = MusteriDetayliPopup(self.popup, self.musteri_verisi)
        except Exception as e:
            messagebox.showerror("Hata", f"Detaylı görünüm açılırken hata oluştu: {e}")
    
    def _edit_customer(self):
        """Müşteri düzenleme penceresi"""
        try:
            edit_popup = MusteriDuzenlePopup(self.popup, self.musteri_verisi)
            # Düzenleme sonrası verileri yenile
            self._load_musteri_data()
        except Exception as e:
            messagebox.showerror("Hata", f"Müşteri düzenleme açılırken hata oluştu: {e}")


class MusteriDetayliPopup:
    """Detaylı müşteri bilgileri popup'ı"""
    
    def __init__(self, parent, musteri_verisi: Dict[str, Any]):
        self.parent = parent
        self.musteri_verisi = musteri_verisi
        
        # Popup penceresi
        self.popup = tk.Toplevel(parent)
        self.popup.title("Detaylı Müşteri Bilgileri")
        self.popup.geometry("800x900")
        self.popup.resizable(True, True)
        
        self.popup.transient(parent)
        self.popup.grab_set()
        
        # Notebook (sekmeli görünüm)
        self.notebook = ttk.Notebook(self.popup)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_tabs()
    
    def _create_tabs(self):
        """Sekmeleri oluştur"""
        # Kullanım Geçmişi sekmesi
        usage_frame = ttk.Frame(self.notebook)
        self.notebook.add(usage_frame, text="📊 Kullanım Geçmişi")
        self._create_usage_tab(usage_frame)
        
        # Fatura Geçmişi sekmesi
        billing_frame = ttk.Frame(self.notebook)
        self.notebook.add(billing_frame, text="💰 Fatura Geçmişi")
        self._create_billing_tab(billing_frame)
        
        # Geçmiş Görüşmeler sekmesi
        gorusmeler_frame = ttk.Frame(self.notebook)
        self.notebook.add(gorusmeler_frame, text="📞 Geçmiş Görüşmeler")
        self._create_gorusmeler_tab(gorusmeler_frame)
        
        # Kampanya Bilgileri sekmesi
        campaign_frame = ttk.Frame(self.notebook)
        self.notebook.add(campaign_frame, text="🎯 Kampanya Bilgileri")
        self._create_campaign_tab(campaign_frame)
        
        # Teknik Bilgiler sekmesi
        tech_frame = ttk.Frame(self.notebook)
        self.notebook.add(tech_frame, text="🔧 Teknik Bilgiler")
        self._create_tech_tab(tech_frame)
    
    def _create_usage_tab(self, parent):
        """Kullanım geçmişi sekmesi"""
        # Treeview ile kullanım geçmişi
        columns = ("Ay", "Dakika", "SMS", "İnternet (MB)", "Yurt Dışı (dk)", "Ödeme (TL)")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        # Sütun başlıkları
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Verileri yükle
        son_4_ay = self.musteri_verisi.get("son_4_aylik_kullanim", [])
        for ay_veri in son_4_ay:
            tree.insert("", tk.END, values=(
                ay_veri.get("ay", "Bilinmiyor"),
                ay_veri.get("konusma_dakika", 0),
                ay_veri.get("sms", 0),
                ay_veri.get("data_mb", 0),
                ay_veri.get("yurt_dişi_dakika", 0),
                ay_veri.get("odeme_tl", 0)
            ))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_billing_tab(self, parent):
        """Fatura geçmişi sekmesi"""
        # Fatura detayları
        text_widget = tk.Text(parent, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Fatura bilgilerini yaz
        son_4_ay = self.musteri_verisi.get("son_4_aylik_kullanim", [])
        text_widget.insert(tk.END, "📋 FATURA GEÇMİŞİ\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        for i, ay_veri in enumerate(son_4_ay, 1):
            text_widget.insert(tk.END, f"📅 {ay_veri.get('ay', 'Bilinmiyor')}\n")
            text_widget.insert(tk.END, f"   💰 Tutar: {ay_veri.get('odeme_tl', 0)} TL\n")
            text_widget.insert(tk.END, f"   📞 Dakika: {ay_veri.get('konusma_dakika', 0)} dk\n")
            text_widget.insert(tk.END, f"   💬 SMS: {ay_veri.get('sms', 0)} adet\n")
            text_widget.insert(tk.END, f"   🌐 İnternet: {ay_veri.get('data_mb', 0)} MB\n")
            text_widget.insert(tk.END, f"   🌍 Yurt Dışı: {ay_veri.get('yurt_dişi_dakika', 0)} dk\n")
            text_widget.insert(tk.END, f"   ✅ Ödendi: {'Evet' if ay_veri.get('odendi_mi', True) else 'Hayır'}\n")
            text_widget.insert(tk.END, "\n")
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_campaign_tab(self, parent):
        """Kampanya bilgileri sekmesi"""
        text_widget = tk.Text(parent, wrap=tk.WORD, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Kampanya bilgilerini yaz
        text_widget.insert(tk.END, "🎯 KAMPANYA BİLGİLERİ\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        # Aktif kampanya
        aktif_kampanya = self.musteri_verisi.get("aktif_kampanya", {})
        if aktif_kampanya:
            text_widget.insert(tk.END, "🔥 AKTİF KAMPANYA\n")
            text_widget.insert(tk.END, f"   📝 Adı: {aktif_kampanya.get('kampanyaAdi', 'Belirtilmemiş')}\n")
            text_widget.insert(tk.END, f"   💰 İndirim: %{aktif_kampanya.get('indirimYüzdesi', 0)}\n")
            text_widget.insert(tk.END, f"   📅 Geçerlilik: {aktif_kampanya.get('gecerlilikTarihi', 'Belirtilmemiş')}\n")
            text_widget.insert(tk.END, f"   📋 Açıklama: {aktif_kampanya.get('aciklama', 'Belirtilmemiş')}\n\n")
        
        # Geçiş yapılabilecek paketler
        gecis_paketler = self.musteri_verisi.get("gecis_yapilabilecek_paketler", [])
        if gecis_paketler:
            text_widget.insert(tk.END, "🔄 GEÇİŞ YAPILABİLECEK PAKETLER\n")
            text_widget.insert(tk.END, "=" * 50 + "\n\n")
            
            for i, paket in enumerate(gecis_paketler, 1):
                text_widget.insert(tk.END, f"{i}. 📦 {paket.get('paketİsmi', 'Belirtilmemiş')}\n")
                text_widget.insert(tk.END, f"   💰 Fiyat: {paket.get('fiyatı', 0)} TL\n")
                text_widget.insert(tk.END, f"   📞 Dakika: {paket.get('dakika', 0)} dk\n")
                text_widget.insert(tk.END, f"   💬 SMS: {paket.get('sms', 0)} adet\n")
                text_widget.insert(tk.END, f"   🌐 İnternet: {paket.get('data_gb', 0)} GB\n")
                
                artilar = paket.get("artiları", [])
                if artilar:
                    text_widget.insert(tk.END, f"   ✨ Artıları: {', '.join(artilar)}\n")
                
                text_widget.insert(tk.END, "\n")
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_tech_tab(self, parent):
        """Teknik bilgiler sekmesi"""
        text_widget = tk.Text(parent, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Teknik bilgileri yaz
        text_widget.insert(tk.END, "🔧 TEKNİK BİLGİLER\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        text_widget.insert(tk.END, "📱 CİHAZ BİLGİLERİ\n")
        text_widget.insert(tk.END, f"   📱 Model: {self.musteri_verisi.get('cihaz_modeli', 'Belirtilmemiş')}\n")
        text_widget.insert(tk.END, f"   🔢 IMEI: {self.musteri_verisi.get('imei', 'Belirtilmemiş')}\n")
        text_widget.insert(tk.END, f"   📶 Şebeke: {self.musteri_verisi.get('sebeke_tipi', 'Belirtilmemiş')}\n")
        text_widget.insert(tk.END, f"   📡 Sinyal Gücü: {self.musteri_verisi.get('sinyal_gucu', 'Belirtilmemiş')}\n\n")
        
        text_widget.insert(tk.END, "🔐 GÜVENLİK BİLGİLERİ\n")
        text_widget.insert(tk.END, f"   🔑 SIM Şifresi: {self.musteri_verisi.get('sim_sifre', 'Belirtilmemiş')}\n")
        text_widget.insert(tk.END, f"   🔒 PUK Kodu: {self.musteri_verisi.get('puk_kodu', 'Belirtilmemiş')}\n")
        text_widget.insert(tk.END, f"   🛡️ Güvenlik Durumu: {self.musteri_verisi.get('guvenlik_durumu', 'Belirtilmemiş')}\n\n")
        
        text_widget.insert(tk.END, "⚙️ SİSTEM BİLGİLERİ\n")
        text_widget.insert(tk.END, f"   📅 Kayıt Tarihi: {self.musteri_verisi.get('kayit_tarihi', 'Belirtilmemiş')}\n")
        text_widget.insert(tk.END, f"   🔄 Son Güncelleme: {self.musteri_verisi.get('son_guncelleme', 'Belirtilmemiş')}\n")
        text_widget.insert(tk.END, f"   🏷️ Müşteri Tipi: {self.musteri_verisi.get('musteri_tipi', 'Belirtilmemiş')}\n")
        text_widget.insert(tk.END, f"   📊 Risk Skoru: {self.musteri_verisi.get('risk_skoru', 'Belirtilmemiş')}\n")
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_gorusmeler_tab(self, parent):
        """Geçmiş görüşmeler sekmesi"""
        if not gecmis_yoneticisi:
            # Geçmiş yöneticisi yoksa uyarı göster
            ttk.Label(parent, text="Geçmiş görüşmeler modülü bulunamadı.", 
                     font=("Arial", 12)).pack(pady=50)
            return
        
        # Ana frame
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Başlık ve istatistikler
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header_frame, text="📞 Geçmiş Görüşmeler", 
                 font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # İstatistikler
        stats_frame = ttk.Frame(header_frame)
        stats_frame.pack(side=tk.RIGHT)
        
        musteri_telefon = self.musteri_verisi.get("numara", "")
        musteri_gorusmeleri = gecmis_yoneticisi.musteri_gecmis_getir(musteri_telefon)
        
        ttk.Label(stats_frame, text=f"Toplam: {len(musteri_gorusmeleri)} görüşme", 
                 font=("Arial", 10)).pack(side=tk.RIGHT)
        
        # Görüşmeler listesi
        if musteri_gorusmeleri:
            # Treeview ile görüşmeler
            columns = ("Tarih", "Süre", "Durum", "Kategoriler", "Sonuç")
            tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=12)
            
            # Sütun başlıkları
            tree.heading("Tarih", text="Tarih")
            tree.heading("Süre", text="Süre (dk)")
            tree.heading("Durum", text="Durum")
            tree.heading("Kategoriler", text="Kategoriler")
            tree.heading("Sonuç", text="Sonuç")
            
            # Sütun genişlikleri
            tree.column("Tarih", width=120)
            tree.column("Süre", width=80)
            tree.column("Durum", width=100)
            tree.column("Kategoriler", width=150)
            tree.column("Sonuç", width=100)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Verileri yükle
            for gorusme in musteri_gorusmeleri:
                # Tarih formatla
                tarih = datetime.fromisoformat(gorusme["baslangic_zamani"]).strftime("%d.%m.%Y %H:%M")
                
                # Süre
                sure = gorusme.get("sure_dakika", 0)
                sure_text = f"{sure} dk" if sure > 0 else "Devam ediyor"
                
                # Durum
                durum = gorusme.get("durum", "bilinmiyor")
                durum_text = "✅ Tamamlandı" if durum == "tamamlandi" else "🔄 Aktif" if durum == "aktif" else "❓ Bilinmiyor"
                
                # Kategoriler
                kategoriler = gorusme.get("kategoriler", [])
                kategori_text = ", ".join(kategoriler) if kategoriler else "Belirtilmemiş"
                
                # Sonuç
                sonuc = gorusme.get("sonuc", "")
                sonuc_text = sonuc[:20] + "..." if len(sonuc) > 20 else sonuc if sonuc else "Belirtilmemiş"
                
                tree.insert("", tk.END, values=(
                    tarih, sure_text, durum_text, kategori_text, sonuc_text
                ), tags=(gorusme["id"],))
            
            # Çift tıklama ile detay göster
            tree.bind("<Double-1>", lambda e: self._show_gorusme_detay(tree))
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Butonlar
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=(10, 0))
            
            ttk.Button(button_frame, text="📋 Detay Gör", 
                      command=lambda: self._show_gorusme_detay(tree)).pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Button(button_frame, text="🔍 Arama", 
                      command=self._show_gorusme_arama).pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Button(button_frame, text="📊 İstatistikler", 
                      command=self._show_gorusme_istatistikleri).pack(side=tk.LEFT)
            
        else:
            # Görüşme yoksa mesaj göster
            ttk.Label(main_frame, text="Bu müşteri için henüz görüşme kaydı bulunmamaktadır.", 
                     font=("Arial", 12)).pack(pady=50)
    
    def _show_gorusme_detay(self, tree):
        """Seçili görüşmenin detaylarını göster"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir görüşme seçin.")
            return
        
        item = tree.item(selection[0])
        gorusme_id = item["tags"][0] if item["tags"] else None
        
        if not gorusme_id or not gecmis_yoneticisi:
            return
        
        # Görüşme detaylarını bul
        musteri_telefon = self.musteri_verisi.get("numara", "")
        musteri_gorusmeleri = gecmis_yoneticisi.musteri_gecmis_getir(musteri_telefon)
        
        gorusme = None
        for g in musteri_gorusmeleri:
            if g["id"] == gorusme_id:
                gorusme = g
                break
        
        if not gorusme:
            return
        
        # Detay popup'ı oluştur
        detail_popup = tk.Toplevel(self.popup)
        detail_popup.title(f"Görüşme Detayı - {gorusme['musteri_adi']}")
        detail_popup.geometry("700x600")
        detail_popup.transient(self.popup)
        detail_popup.grab_set()
        
        # İçerik
        text_widget = tk.Text(detail_popup, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(detail_popup, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Görüşme bilgilerini yaz
        text_widget.insert(tk.END, "📞 GÖRÜŞME DETAYI\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        text_widget.insert(tk.END, f"👤 Müşteri: {gorusme['musteri_adi']}\n")
        text_widget.insert(tk.END, f"📱 Telefon: {gorusme['musteri_telefon']}\n")
        text_widget.insert(tk.END, f"📅 Başlangıç: {datetime.fromisoformat(gorusme['baslangic_zamani']).strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        if gorusme.get("bitis_zamani"):
            text_widget.insert(tk.END, f"⏰ Bitiş: {datetime.fromisoformat(gorusme['bitis_zamani']).strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        text_widget.insert(tk.END, f"⏱️ Süre: {gorusme.get('sure_dakika', 0)} dakika\n")
        text_widget.insert(tk.END, f"📊 Durum: {gorusme.get('durum', 'bilinmiyor')}\n")
        
        kategoriler = gorusme.get("kategoriler", [])
        if kategoriler:
            text_widget.insert(tk.END, f"🏷️ Kategoriler: {', '.join(kategoriler)}\n")
        
        if gorusme.get("memnuniyet_puani"):
            text_widget.insert(tk.END, f"⭐ Memnuniyet: {gorusme['memnuniyet_puani']}/5\n")
        
        if gorusme.get("sonuc"):
            text_widget.insert(tk.END, f"📋 Sonuç: {gorusme['sonuc']}\n")
        
        if gorusme.get("notlar"):
            text_widget.insert(tk.END, f"📝 Notlar: {gorusme['notlar']}\n")
        
        text_widget.insert(tk.END, "\n💬 MESAJLAR\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        mesajlar = gorusme.get("mesajlar", [])
        if mesajlar:
            for mesaj in mesajlar:
                zaman = datetime.fromisoformat(mesaj["zaman"]).strftime("%H:%M:%S")
                gonderen = mesaj["gonderen"]
                mesaj_metni = mesaj["mesaj"]
                
                text_widget.insert(tk.END, f"[{zaman}] {gonderen}: {mesaj_metni}\n")
        else:
            text_widget.insert(tk.END, "Henüz mesaj kaydı bulunmamaktadır.\n")
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Kapat butonu
        ttk.Button(detail_popup, text="Kapat", command=detail_popup.destroy).pack(pady=10)
    
    def _show_gorusme_arama(self):
        """Görüşme arama popup'ı"""
        if not gecmis_yoneticisi:
            messagebox.showwarning("Uyarı", "Geçmiş görüşmeler modülü bulunamadı.")
            return
        
        # Arama popup'ı
        search_popup = tk.Toplevel(self.popup)
        search_popup.title("Görüşme Arama")
        search_popup.geometry("500x400")
        search_popup.transient(self.popup)
        search_popup.grab_set()
        
        # Arama frame
        search_frame = ttk.Frame(search_popup, padding="10")
        search_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(search_frame, text="🔍 Görüşme Arama", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # Arama kutusu
        ttk.Label(search_frame, text="Arama terimi:").pack(anchor=tk.W)
        search_entry = ttk.Entry(search_frame, width=50)
        search_entry.pack(fill=tk.X, pady=(0, 10))
        search_entry.focus()
        
        # Sonuçlar
        results_frame = ttk.Frame(search_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Arama fonksiyonu
        def perform_search():
            term = search_entry.get().strip()
            if not term:
                return
            
            results = gecmis_yoneticisi.gorusme_ara(term)
            
            # Sonuçları göster
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            if results:
                ttk.Label(results_frame, text=f"{len(results)} sonuç bulundu:", 
                         font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
                
                for gorusme in results[:10]:  # İlk 10 sonuç
                    tarih = datetime.fromisoformat(gorusme["baslangic_zamani"]).strftime("%d.%m.%Y %H:%M")
                    frame = ttk.Frame(results_frame)
                    frame.pack(fill=tk.X, pady=2)
                    
                    ttk.Label(frame, text=f"{tarih} - {gorusme['musteri_adi']}", 
                             font=("Arial", 9)).pack(side=tk.LEFT)
                    
                    ttk.Button(frame, text="Detay", 
                              command=lambda g=gorusme: self._show_gorusme_detay_from_search(g, search_popup)).pack(side=tk.RIGHT)
            else:
                ttk.Label(results_frame, text="Sonuç bulunamadı.", 
                         font=("Arial", 10)).pack(pady=20)
        
        search_entry.bind("<Return>", lambda e: perform_search())
        ttk.Button(search_frame, text="Ara", command=perform_search).pack(pady=10)
    
    def _show_gorusme_detay_from_search(self, gorusme, parent_popup):
        """Arama sonucundan görüşme detayı göster"""
        parent_popup.destroy()
        
        # Detay popup'ı oluştur
        detail_popup = tk.Toplevel(self.popup)
        detail_popup.title(f"Görüşme Detayı - {gorusme['musteri_adi']}")
        detail_popup.geometry("700x600")
        detail_popup.transient(self.popup)
        detail_popup.grab_set()
        
        # İçerik
        text_widget = tk.Text(detail_popup, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(detail_popup, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Görüşme bilgilerini yaz
        text_widget.insert(tk.END, "📞 GÖRÜŞME DETAYI\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        text_widget.insert(tk.END, f"👤 Müşteri: {gorusme['musteri_adi']}\n")
        text_widget.insert(tk.END, f"📱 Telefon: {gorusme['musteri_telefon']}\n")
        text_widget.insert(tk.END, f"📅 Başlangıç: {datetime.fromisoformat(gorusme['baslangic_zamani']).strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        if gorusme.get("bitis_zamani"):
            text_widget.insert(tk.END, f"⏰ Bitiş: {datetime.fromisoformat(gorusme['bitis_zamani']).strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        text_widget.insert(tk.END, f"⏱️ Süre: {gorusme.get('sure_dakika', 0)} dakika\n")
        text_widget.insert(tk.END, f"📊 Durum: {gorusme.get('durum', 'bilinmiyor')}\n")
        
        kategoriler = gorusme.get("kategoriler", [])
        if kategoriler:
            text_widget.insert(tk.END, f"🏷️ Kategoriler: {', '.join(kategoriler)}\n")
        
        if gorusme.get("memnuniyet_puani"):
            text_widget.insert(tk.END, f"⭐ Memnuniyet: {gorusme['memnuniyet_puani']}/5\n")
        
        if gorusme.get("sonuc"):
            text_widget.insert(tk.END, f"📋 Sonuç: {gorusme['sonuc']}\n")
        
        if gorusme.get("notlar"):
            text_widget.insert(tk.END, f"📝 Notlar: {gorusme['notlar']}\n")
        
        text_widget.insert(tk.END, "\n💬 MESAJLAR\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        mesajlar = gorusme.get("mesajlar", [])
        if mesajlar:
            for mesaj in mesajlar:
                zaman = datetime.fromisoformat(mesaj["zaman"]).strftime("%H:%M:%S")
                gonderen = mesaj["gonderen"]
                mesaj_metni = mesaj["mesaj"]
                
                text_widget.insert(tk.END, f"[{zaman}] {gonderen}: {mesaj_metni}\n")
        else:
            text_widget.insert(tk.END, "Henüz mesaj kaydı bulunmamaktadır.\n")
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Kapat butonu
        ttk.Button(detail_popup, text="Kapat", command=detail_popup.destroy).pack(pady=10)
    
    def _show_gorusme_istatistikleri(self):
        """Görüşme istatistikleri popup'ı"""
        if not gecmis_yoneticisi:
            messagebox.showwarning("Uyarı", "Geçmiş görüşmeler modülü bulunamadı.")
            return
        
        stats = gecmis_yoneticisi.istatistikleri_getir()
        
        # İstatistik popup'ı
        stats_popup = tk.Toplevel(self.popup)
        stats_popup.title("Görüşme İstatistikleri")
        stats_popup.geometry("400x300")
        stats_popup.transient(self.popup)
        stats_popup.grab_set()
        
        # İçerik
        content_frame = ttk.Frame(stats_popup, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content_frame, text="📊 Görüşme İstatistikleri", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # İstatistikler
        stats_data = [
            ("📞 Toplam Görüşme", stats.get("toplam_gorusme", 0)),
            ("📅 Bu Ay", stats.get("bu_ay", 0)),
            ("📆 Bu Hafta", stats.get("bu_hafta", 0)),
            ("📅 Bugün", stats.get("bugun", 0))
        ]
        
        for label, value in stats_data:
            frame = ttk.Frame(content_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label, font=("Arial", 12)).pack(side=tk.LEFT)
            ttk.Label(frame, text=str(value), font=("Arial", 12, "bold")).pack(side=tk.RIGHT)
        
        ttk.Button(content_frame, text="Kapat", command=stats_popup.destroy).pack(pady=20)


class MusteriDuzenlePopup:
    """Müşteri düzenleme popup'ı"""
    
    def __init__(self, parent, musteri_verisi: Dict[str, Any]):
        self.parent = parent
        self.musteri_verisi = musteri_verisi.copy()
        
        # Popup penceresi
        self.popup = tk.Toplevel(parent)
        self.popup.title("Müşteri Bilgilerini Düzenle")
        self.popup.geometry("500x600")
        self.popup.resizable(True, True)
        
        self.popup.transient(parent)
        self.popup.grab_set()
        
        # Ana frame
        main_frame = ttk.Frame(self.popup, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(
            main_frame, 
            text="✏️ Müşteri Bilgilerini Düzenle", 
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Form alanları
        self._create_form_fields(main_frame)
        
        # Butonlar
        self._create_buttons(main_frame)
        
        # Form verilerini yükle
        self._load_form_data()
    
    def _create_form_fields(self, parent):
        """Form alanlarını oluştur"""
        # Form frame
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form alanları
        self.form_entries = {}
        
        fields = [
            ("Ad Soyad:", "ad"),
            ("Telefon:", "numara"),
            ("E-posta:", "email"),
            ("Adres:", "adres"),
            ("TC Kimlik:", "tc")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(form_frame, text=label_text, font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
            
            if field_name == "adres":
                # Adres için çok satırlı text widget
                entry = tk.Text(form_frame, height=3, width=50)
            else:
                entry = ttk.Entry(form_frame, width=50)
            
            entry.pack(fill=tk.X, pady=(0, 10))
            self.form_entries[field_name] = entry
    
    def _create_buttons(self, parent):
        """Butonları oluştur"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        # Kaydet butonu
        save_btn = ttk.Button(
            button_frame, 
            text="💾 Kaydet", 
            command=self._save_changes,
            style="Accent.TButton"
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # İptal butonu
        cancel_btn = ttk.Button(
            button_frame, 
            text="❌ İptal", 
            command=self.popup.destroy
        )
        cancel_btn.pack(side=tk.LEFT)
    
    def _load_form_data(self):
        """Form verilerini yükle"""
        try:
            # Temel bilgileri yükle
            self.form_entries["ad"].insert(0, self.musteri_verisi.get("ad", ""))
            self.form_entries["numara"].insert(0, self.musteri_verisi.get("numara", ""))
            self.form_entries["email"].insert(0, self.musteri_verisi.get("email", ""))
            self.form_entries["tc"].insert(0, self.musteri_verisi.get("tc", ""))
            
            # Adres için text widget
            adres = self.musteri_verisi.get("adres", "")
            self.form_entries["adres"].insert("1.0", adres)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Form verileri yüklenirken hata oluştu: {e}")
    
    def _save_changes(self):
        """Değişiklikleri kaydet"""
        try:
            # Form verilerini al
            self.musteri_verisi["ad"] = self.form_entries["ad"].get()
            self.musteri_verisi["numara"] = self.form_entries["numara"].get()
            self.musteri_verisi["email"] = self.form_entries["email"].get()
            self.musteri_verisi["tc"] = self.form_entries["tc"].get()
            self.musteri_verisi["adres"] = self.form_entries["adres"].get("1.0", tk.END).strip()
            
            # Verileri kaydet (gerçek uygulamada veritabanına kaydedilir)
            # Burada sadece mesaj gösteriyoruz
            messagebox.showinfo("Başarılı", "Müşteri bilgileri güncellendi!")
            
            # Popup'ı kapat
            self.popup.destroy()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Değişiklikler kaydedilirken hata oluştu: {e}")


def show_musteri_popup(parent, musteri_verisi: Dict[str, Any]):
    """Müşteri popup'ını göster"""
    try:
        popup = MusteriPopup(parent, musteri_verisi)
        return popup
    except Exception as e:
        messagebox.showerror("Hata", f"Popup açılırken hata oluştu: {e}")
        return None
