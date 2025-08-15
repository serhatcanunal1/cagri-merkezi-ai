#!/usr/bin/env python3
"""
Call Center UI - Modern User Interface
This module provides the advanced UI design and detailed customer analytics.

Developed by Trivox Team:
- Serhatcan Ünal, Elif Zeynep Tosun, Meryem Gençali, Ali Buğrahan Budak

Features:
- Real-time conversation display
- Live system logs with color coding
- Customer profile and history management
- Modern dark theme (Catppuccin-inspired)
- Scrollable conversation history
- System statistics and analytics

Ultra Modern Çağrı Merkezi UI - Gelişmiş Arayüz
Gelişmiş tasarım ve detaylı müşteri analizi sağlar.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
import json
from typing import Dict, List, Optional
import logging

# Geçmiş görüşmeler modülünü import et
try:
    from conversation_history import gecmis_yoneticisi
except ImportError:
    print("Uyarı: conversation_history.py bulunamadı. Geçmiş görüşmeler özelliği devre dışı.")
    gecmis_yoneticisi = None

class UILogHandler(logging.Handler):
    """UI log paneline mesaj gönderen custom handler"""
    def __init__(self, ui_instance):
        super().__init__()
        self.ui = ui_instance
    
    def emit(self, record):
        """Log mesajını UI'ya gönder"""
        try:
            # Log level'a göre tip belirle
            level_map = {
                logging.DEBUG: "DEBUG",
                logging.INFO: "INFO", 
                logging.WARNING: "WARNING",
                logging.ERROR: "ERROR",
                logging.CRITICAL: "ERROR"
            }
            log_type = level_map.get(record.levelno, "INFO")
            
            # Log mesajını UI'ya ekle
            if hasattr(self.ui, 'add_system_log'):
                self.ui.add_system_log(record.getMessage(), log_type)
        except Exception:
            pass  # Log handler'da hata olursa sessizce geç

class UltraModernCagriMerkeziUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trivox Çağrı Merkezi Asistan Kontrol Yazılımı")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#11111b')
        
        # Müşteri verisi
        self.musteri_data = None
        self.aktif_gorusme_id = None
        self.current_telefon = None
        
        # UI bileşenleri
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        self.setup_animations()
        
        # İstatistikler
        self.call_count = 0
        self.avg_duration = 0
        self.success_rate = 0
        
        # Durum güncellemeleri
        self.status_update_thread = threading.Thread(target=self._status_update_loop, daemon=True)
        self.status_update_thread.start()
        
        # Log handler'ı ekle
        self.setup_log_handler()
    
    def setup_styles(self):
        """Ultra modern stil ayarları"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Ana renkler - Modern gradyan tema
        style.configure('Main.TFrame', background='#1e1e2e')  # Ana chat paneli - mor tonlu
        style.configure('Log.TFrame', background='#0d1117')   # Log paneli - GitHub koyu
        style.configure('Sidebar.TFrame', background='#181825') # Müşteri paneli - koyu mavi
        style.configure('Card.TFrame', background='#313244', relief='flat', borderwidth=1)
        style.configure('Status.TFrame', background='#11111b')
        style.configure('Customer.TFrame', background='#313244')
        style.configure('History.TFrame', background='#262637')
        
        # Butonlar - Modern gradyan efektleri
        style.configure('Primary.TButton', 
                       background='#89b4fa', 
                       foreground='#11111b',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background='#a6e3a1',
                       foreground='#11111b',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Warning.TButton',
                       background='#f9e2af',
                       foreground='#11111b',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Danger.TButton',
                       background='#f38ba8',
                       foreground='#11111b',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Info.TButton',
                       background='#74c7ec',
                       foreground='#11111b',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        # Label'lar - Modern tipografi
        style.configure('Title.TLabel',
                       background='#313244',
                       foreground='#cdd6f4',
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background='#313244',
                       foreground='#bac2de',
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Info.TLabel',
                       background='#313244',
                       foreground='#a6adc8',
                       font=('Segoe UI', 10))
        
        style.configure('Status.TLabel',
                       background='#11111b',
                       foreground='#a6e3a1',
                       font=('Consolas', 10, 'bold'))
        
        style.configure('Customer.TLabel',
                       background='#313244',
                       foreground='#cdd6f4',
                       font=('Segoe UI', 11))
        
        style.configure('History.TLabel',
                       background='#262637',
                       foreground='#bac2de',
                       font=('Segoe UI', 9))
        
        # Scrollbar stili - daha görünür
        style.configure('Vertical.TScrollbar',
                       background='#45475a',         # Daha açık gri
                       troughcolor='#181825',        # Koyu kanal
                       borderwidth=2,                # Kalın kenar çizgisi
                       arrowcolor='#cdd6f4',         # Açık ok rengi
                       darkcolor='#45475a',          
                       lightcolor='#585b70',         # Daha açık renk
                       relief='raised',              # Yükseltilmiş görünüm
                       gripcount=0)                  # Grip işaretleri kaldır
        
        # Scrollbar boyutu için map stili
        style.map('Vertical.TScrollbar',
                 background=[('active', '#74c7ec'),     # Mavi hover rengi
                            ('pressed', '#89b4fa')],    # Daha açık mavi tıklama rengi
                 relief=[('pressed', 'sunken'),         # Tıklandığında çukur görünüm
                        ('!pressed', 'raised')])        # Normal durumda yüksek görünüm
    
    def create_widgets(self):
        """Ana widget'ları oluştur"""
        
        # Ana container
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        
        # Ana 3 panel düzeni: Loglar (sol) | Chat (orta) | Müşteri (sağ)
        self.system_log_container = ttk.Frame(self.main_container, style='Log.TFrame', width=400)
        self.chat_container = ttk.Frame(self.main_container, style='Main.TFrame')
        # Müşteri paneli zaten var (self.right_panel)
        
        # Üst durum çubuğu
        self.status_bar = ttk.Frame(self.chat_container, style='Status.TFrame', height=80)
        self.status_label = ttk.Label(self.status_bar, text="🟢 Sistem Hazır", 
                                     style='Status.TLabel')
        self.call_stats = ttk.Label(self.status_bar, text="📞 Toplam Çağrı: 0", 
                                   style='Status.TLabel')
        
        # Chat alanı
        self.chat_frame = ttk.Frame(self.chat_container, style='Card.TFrame')
        self.chat_title = ttk.Label(self.chat_frame, text="💬 Canlı Görüşme", 
                                   style='Title.TLabel')
        
        # Chat alanı için canvas ve scrollbar
        self.chat_canvas = tk.Canvas(self.chat_frame, bg='#1e1e2e', highlightthickness=0)
        self.chat_scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_scrollable_frame = ttk.Frame(self.chat_canvas, style='Card.TFrame')
        
        self.chat_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )
        
        self.chat_canvas.create_window((0, 0), window=self.chat_scrollable_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        
        # Alt kontrol paneli
        self.control_panel = ttk.Frame(self.chat_container, style='Status.TFrame', height=100)
        
        # Sol butonlar
        self.left_buttons = ttk.Frame(self.control_panel, style='Status.TFrame')
        self.start_btn = ttk.Button(self.left_buttons, text="▶️ Çağrı Başlat", 
                                   style='Success.TButton', command=self.start_call)
        self.stop_btn = ttk.Button(self.left_buttons, text="⏹️ Çağrı Durdur", 
                                  style='Danger.TButton', command=self.stop_call, state='disabled')
        
        # Orta butonlar
        self.center_buttons = ttk.Frame(self.control_panel, style='Status.TFrame')
        self.gecmis_btn = ttk.Button(self.center_buttons, text="📋 Geçmiş Görüşmeler", 
                                    style='Primary.TButton', command=self._show_gecmis_gorusmeler)
        self.istatistik_btn = ttk.Button(self.center_buttons, text="📊 İstatistikler", 
                                        style='Primary.TButton', command=self._show_istatistikler)
        
        # Sağ butonlar
        self.right_buttons = ttk.Frame(self.control_panel, style='Status.TFrame')
        self.ayarlar_btn = ttk.Button(self.right_buttons, text="⚙️ Ayarlar", 
                                     style='Warning.TButton', command=self._show_ayarlar)
        self.cikis_btn = ttk.Button(self.right_buttons, text="🚪 Çıkış", 
                                   style='Danger.TButton', command=self._exit_application)
        
        # Sistem Log Paneli
        self.create_system_log_panel()
        
        # Sağ panel - Müşteri bilgileri
        self.right_panel = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=500)
        
        # Müşteri başlık
        self.customer_header = ttk.Frame(self.right_panel, style='Customer.TFrame')
        self.customer_title = ttk.Label(self.customer_header, text="👤 Müşteri Profili", 
                                       style='Title.TLabel')
        
        # Müşteri temel bilgileri
        self.customer_basic = ttk.Frame(self.right_panel, style='Customer.TFrame')
        self.customer_name = ttk.Label(self.customer_basic, text="Müşteri Seçilmedi", 
                                      style='Customer.TLabel')
        self.customer_phone = ttk.Label(self.customer_basic, text="", 
                                       style='Customer.TLabel')
        self.customer_status = ttk.Label(self.customer_basic, text="", 
                                        style='Customer.TLabel')
        
        # Müşteri detay kartları
        self.customer_details = ttk.Frame(self.right_panel, style='Customer.TFrame')
        
        # Paket bilgileri kartı
        self.paket_card = ttk.Frame(self.customer_details, style='Card.TFrame')
        self.paket_title = ttk.Label(self.paket_card, text="📦 Paket Bilgileri", 
                                    style='Subtitle.TLabel')
        self.paket_info = ttk.Label(self.paket_card, text="Paket bilgisi yok", 
                                   style='Info.TLabel', wraplength=450)
        
        # Kullanım bilgileri kartı
        self.kullanim_card = ttk.Frame(self.customer_details, style='Card.TFrame')
        self.kullanim_title = ttk.Label(self.kullanim_card, text="📊 Kullanım Bilgileri", 
                                       style='Subtitle.TLabel')
        self.kullanim_info = ttk.Label(self.kullanim_card, text="Kullanım bilgisi yok", 
                                      style='Info.TLabel', wraplength=450)
        
        # Fatura bilgileri kartı
        self.fatura_card = ttk.Frame(self.customer_details, style='Card.TFrame')
        self.fatura_title = ttk.Label(self.fatura_card, text="💰 Fatura Bilgileri", 
                                     style='Subtitle.TLabel')
        self.fatura_info = ttk.Label(self.fatura_card, text="Fatura bilgisi yok", 
                                    style='Info.TLabel', wraplength=450)
        
        # Müşteri analizi kartı
        self.analiz_card = ttk.Frame(self.customer_details, style='Card.TFrame')
        self.analiz_title = ttk.Label(self.analiz_card, text="📈 Müşteri Analizi", 
                                     style='Subtitle.TLabel')
        self.analiz_info = ttk.Label(self.analiz_card, text="Analiz bilgisi yok", 
                                    style='Info.TLabel', wraplength=450)
        
        # Geçmiş görüşmeler bölümü
        self.history_section = ttk.Frame(self.right_panel, style='History.TFrame')
        self.history_title = ttk.Label(self.history_section, text="📞 Geçmiş Görüşmeler", 
                                      style='Subtitle.TLabel')
        
        # Geçmiş görüşmeler listesi
        self.history_frame = ttk.Frame(self.history_section, style='History.TFrame')
        self.history_canvas = tk.Canvas(self.history_frame, bg='#262637', highlightthickness=0, height=200)
        self.history_scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_canvas.yview)
        
        # Scrollbar stilini ayarla (width ttk.Scrollbar'da desteklenmiyor)
        self.history_scrollable_frame = ttk.Frame(self.history_canvas, style='History.TFrame')
        
        self.history_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(scrollregion=(0, 0, 0, self.history_scrollable_frame.winfo_reqheight()))
        )
        
        self.history_canvas.create_window((0, 0), window=self.history_scrollable_frame, anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.history_scrollbar.set)
        
        # Mouse wheel desteği
        def _on_mousewheel(event):
            self.history_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.history_canvas.bind("<MouseWheel>", _on_mousewheel)
        self.history_scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
    
    def create_system_log_panel(self):
        """Sistem log panelini oluştur"""
        # Log başlık
        self.log_title = ttk.Label(self.system_log_container, text="🔧 Sistem Logları", 
                                  style='Title.TLabel')
        
        # Log alanı için frame
        self.log_frame = ttk.Frame(self.system_log_container, style='Card.TFrame')
        
        # Log text widget
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            height=20,
            width=50,
            bg='#0d1117',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            font=('Consolas', 9),
            wrap=tk.WORD,
            state='disabled'
        )
        
        # Log temizleme butonu
        self.log_clear_btn = ttk.Button(self.system_log_container, text="🗑️ Logları Temizle", 
                                       style='Warning.TButton', command=self.clear_system_logs)
    
    def setup_layout(self):
        """Layout düzenlemesi"""
        # Ana container
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sol panel: Sistem Logları
        self.system_log_container.pack(side='left', fill='both', padx=(0, 5))
        
        # Orta panel: Chat (Canlı Görüşme) 
        self.chat_container.pack(side='left', fill='both', expand=True, padx=5)
        
        # Durum çubuğu
        self.status_bar.pack(fill='x', pady=(0, 10))
        self.status_label.pack(side='left', padx=10, pady=10)
        self.call_stats.pack(side='right', padx=10, pady=10)
        
        # Chat alanı
        self.chat_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.chat_title.pack(pady=(10, 5))
        
        # Chat canvas ve scrollbar
        self.chat_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=(0, 10))
        self.chat_scrollbar.pack(side="right", fill="y", pady=(0, 10))
        
        # Kontrol paneli
        self.control_panel.pack(fill='x')
        
        # Butonlar
        self.left_buttons.pack(side='left', padx=10, pady=10)
        self.start_btn.pack(side='left', padx=5)
        self.stop_btn.pack(side='left', padx=5)
        
        self.center_buttons.pack(side='left', padx=10, pady=10)
        self.gecmis_btn.pack(side='left', padx=5)
        self.istatistik_btn.pack(side='left', padx=5)
        
        self.right_buttons.pack(side='right', padx=10, pady=10)
        self.ayarlar_btn.pack(side='right', padx=5)
        self.cikis_btn.pack(side='right', padx=5)
        
        # Sistem Log Paneli Layout
        self.log_title.pack(pady=(10, 5))
        self.log_frame.pack(fill='both', expand=True, pady=5)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.log_clear_btn.pack(pady=10)
        
        # Sağ panel: Müşteri Bilgileri
        self.right_panel.pack(side='right', fill='both', padx=(5, 0))
        
        # Müşteri başlık
        self.customer_header.pack(fill='x', pady=(0, 10))
        self.customer_title.pack(pady=10)
        
        # Müşteri temel bilgileri
        self.customer_basic.pack(fill='x', pady=(0, 10))
        self.customer_name.pack(pady=(10, 5))
        self.customer_phone.pack(pady=(0, 5))
        self.customer_status.pack(pady=(0, 10))
        
        # Müşteri detayları
        self.customer_details.pack(fill='x', pady=(0, 10))
        
        # Kartlar
        self.paket_card.pack(fill='x', pady=(0, 10))
        self.paket_title.pack(pady=(10, 5))
        self.paket_info.pack(pady=(0, 10), padx=10)
        
        self.kullanim_card.pack(fill='x', pady=(0, 10))
        self.kullanim_title.pack(pady=(10, 5))
        self.kullanim_info.pack(pady=(0, 10), padx=10)
        
        self.fatura_card.pack(fill='x', pady=(0, 10))
        self.fatura_title.pack(pady=(10, 5))
        self.fatura_info.pack(pady=(0, 10), padx=10)
        
        self.analiz_card.pack(fill='x', pady=(0, 10))
        self.analiz_title.pack(pady=(10, 5))
        self.analiz_info.pack(pady=(0, 10), padx=10)
        
        # Geçmiş görüşmeler
        self.history_section.pack(fill='both', expand=True)
        self.history_title.pack(pady=(10, 5))
        
        self.history_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.history_canvas.pack(side="left", fill="both", expand=True)
        # Scrollbar sadece _load_customer_history'de pack edilecek
    
    def setup_animations(self):
        """Animasyon efektleri"""
        # Mouse hover efektleri
        for btn in [self.start_btn, self.stop_btn, self.gecmis_btn, self.istatistik_btn, 
                   self.ayarlar_btn, self.cikis_btn]:
            btn.bind('<Enter>', lambda e, b=btn: self._on_button_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self._on_button_hover(b, False))
    
    def _on_button_hover(self, button, entering):
        """Buton hover efekti"""
        if entering:
            button.configure(style='Primary.TButton')
        else:
            # Orijinal stilini geri yükle
            if button == self.start_btn:
                button.configure(style='Success.TButton')
            elif button == self.stop_btn:
                button.configure(style='Danger.TButton')
            elif button == self.ayarlar_btn:
                button.configure(style='Warning.TButton')
            elif button == self.cikis_btn:
                button.configure(style='Danger.TButton')
            else:
                button.configure(style='Primary.TButton')
    
    def add_message(self, sender, message, message_type="normal"):
        """Chat alanına mesaj ekle"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Mesaj frame'i oluştur
        msg_frame = ttk.Frame(self.chat_scrollable_frame, style='Card.TFrame')
        
        # Gönderen ve zaman
        header_frame = ttk.Frame(msg_frame, style='Card.TFrame')
        sender_label = ttk.Label(header_frame, 
                                text=f"{sender} • {timestamp}", 
                                style='Subtitle.TLabel')
        sender_label.pack(side='left')
        
        # Mesaj içeriği
        message_label = ttk.Label(msg_frame, 
                                 text=message, 
                                 style='Info.TLabel', 
                                 wraplength=800,
                                 justify='left')
        
        # Layout
        header_frame.pack(fill='x', pady=(10, 5), padx=10)
        message_label.pack(fill='x', pady=(0, 10), padx=10)
        msg_frame.pack(fill='x', padx=10, pady=5)
        
        # Scroll to bottom
        self.root.after(100, self._scroll_to_bottom)
        
        # Mesaj tipine göre renk
        if message_type == "system":
            msg_frame.configure(style='Status.TFrame')
        elif message_type == "customer":
            msg_frame.configure(style='Card.TFrame')
        elif message_type == "assistant":
            msg_frame.configure(style='Card.TFrame')
    
    def _scroll_to_bottom(self):
        """Chat alanını en alta kaydır"""
        self.chat_canvas.yview_moveto(1)
    
    def set_musteri_data(self, data):
        """Müşteri verilerini sağ panelde göster"""
        self.musteri_data = data
        # Normalize edilmiş telefon numarasını kullan
        self.current_telefon = data.get("normalized_numara", data.get("numara", ""))
        
        # Temel bilgiler
        ad = data.get("ad", "Bilinmiyor")
        telefon = data.get("numara", "Bilinmiyor")
        tc = data.get("tc", "Bilinmiyor")
        
        self.customer_name.configure(text=f"👤 {ad}")
        self.customer_phone.configure(text=f"📱 {telefon}")
        self.customer_status.configure(text=f"🆔 TC: {tc}")
        
        # Paket bilgileri
        paket = data.get("numaraya_tanimli_paket", {})
        if paket:
            paket_isim = paket.get("paketİsmi", "Bilinmiyor")
            paket_fiyat = paket.get("fiyatı", "Bilinmiyor")
            paket_text = f"📦 {paket_isim}\n💰 {paket_fiyat} TL"
        else:
            paket_text = "Paket bilgisi bulunamadı"
        self.paket_info.configure(text=paket_text)
        
        # Kullanım bilgileri
        kalanlar = data.get("kalan_kullanim_haklari", {})
        if kalanlar:
            kullanim_text = f"⏱️ {kalanlar.get('kalanDakika', 0)} dk\n📱 {kalanlar.get('kalanSms', 0)} SMS\n🌐 {kalanlar.get('kalanİnternet', 0)} GB"
        else:
            kullanim_text = "Kullanım bilgisi bulunamadı"
        self.kullanim_info.configure(text=kullanim_text)
        
        # Fatura bilgileri
        son_odeme = data.get("son_fatura_odeme_tarihi", "Bilinmiyor")
        odendi_mi = data.get("fatura_odendi_mi", None)
        odendi_text = "✅ Ödendi" if odendi_mi else "❌ Ödenmedi" if odendi_mi is False else "❓ Bilinmiyor"
        
        fatura_text = f"📅 Son Ödeme: {son_odeme}\n{odendi_text}"
        self.fatura_info.configure(text=fatura_text)
        
        # Müşteri analizi
        if gecmis_yoneticisi and self.current_telefon:
            analiz = gecmis_yoneticisi.musteri_analizi(self.current_telefon)
            if analiz:
                analiz_text = f"📊 Toplam Görüşme: {analiz.get('toplam_gorusme', 0)}\n"
                analiz_text += f"⏱️ Ortalama Süre: {analiz.get('ortalama_gorusme_suresi', 0):.1f} dk\n"
                analiz_text += f"📅 Son 30 Gün: {analiz.get('son_30_gun_gorusme', 0)} görüşme"
            else:
                analiz_text = "İlk kez görüşülüyor"
        else:
            analiz_text = "Analiz bilgisi yok"
        
        self.analiz_info.configure(text=analiz_text)
        
        # Geçmiş görüşmeleri yükle
        self._load_customer_history()
    
    def _load_customer_history(self):
        """Müşteri geçmiş görüşmelerini yükle"""
        # Mevcut widget'ları temizle
        for widget in self.history_scrollable_frame.winfo_children():
            widget.destroy()
        
        if not gecmis_yoneticisi or not self.current_telefon:
            return
        
        # Müşteri görüşmelerini al (tümünü getir)
        gorusmeler = gecmis_yoneticisi.musteri_gorusmeleri_getir(self.current_telefon, 50)
        
        for gorusme in gorusmeler:
            # Görüşme kartı oluştur
            gorusme_frame = ttk.Frame(self.history_scrollable_frame, style='Card.TFrame')
            
            # Tarih ve süre
            tarih = datetime.fromisoformat(gorusme["baslangic_zamani"]).strftime("%d.%m.%Y %H:%M")
            sure = gorusme.get("sure", 0)
            kategori = gorusme.get("kategori", "Bilinmiyor")
            durum = gorusme.get("durum", "bilinmiyor")
            
            # Başlık
            header = ttk.Frame(gorusme_frame, style='Card.TFrame')
            ttk.Label(header, text=f"📅 {tarih}", style='History.TLabel').pack(side='left')
            ttk.Label(header, text=f"⏱️ {sure:.1f}dk", style='History.TLabel').pack(side='right')
            header.pack(fill='x', pady=(2, 1))
            
            # Kategori ve durum
            details = ttk.Frame(gorusme_frame, style='Card.TFrame')
            ttk.Label(details, text=f"🏷️ {kategori}", style='History.TLabel').pack(side='left')
            durum_icon = "✅" if durum == "tamamlandi" else "🔄" if durum == "aktif" else "❌"
            ttk.Label(details, text=f"{durum_icon} {durum}", style='History.TLabel').pack(side='right')
            details.pack(fill='x', pady=(0, 2))
            
            gorusme_frame.pack(fill='x', padx=3, pady=1)
        
        # Scroll region'ı güncelle
        self.history_scrollable_frame.update_idletasks()
        # Scrollable frame'in gerçek boyutunu kullan
        self.history_canvas.configure(scrollregion=(0, 0, 0, self.history_scrollable_frame.winfo_reqheight()))
        
        # Scrollbar'ı görünür yap
        self.history_scrollbar.pack_forget()  # Önce kaldır
        self.history_scrollbar.pack(side="right", fill="y")  # Sonra ekle
            
        # Debug: Canvas boyutlarını zorla güncelle
        self.history_canvas.update_idletasks()
        # Eğer içerik canvas'tan büyükse scrolling aktif olmalı
        content_height = self.history_scrollable_frame.winfo_reqheight()
        canvas_height = self.history_canvas.winfo_height()
        print(f"DEBUG: Loaded {len(gorusmeler)} conversations")
        print(f"DEBUG: Scrolling info - Content: {content_height}, Canvas: {canvas_height}")
        if content_height > canvas_height:
            print(f"DEBUG: Scrolling NEEDED")
        else:
            print(f"DEBUG: No scrolling needed")
    
    def update_status(self, status, color="green"):
        """Durum çubuğunu güncelle"""
        colors = {
            "green": "🟢",
            "yellow": "🟡", 
            "red": "🔴",
            "blue": "🔵"
        }
        icon = colors.get(color, "🟢")
        self.status_label.configure(text=f"{icon} {status}")
    
    def update_stats(self, call_count=None, avg_duration=None, success_rate=None):
        """İstatistikleri güncelle"""
        if call_count is not None:
            self.call_count = call_count
        if avg_duration is not None:
            self.avg_duration = avg_duration
        if success_rate is not None:
            self.success_rate = success_rate
            
        stats_text = f"📞 Toplam Çağrı: {self.call_count}"
        self.call_stats.configure(text=stats_text)
    
    def start_call(self):
        """Çağrı başlat"""
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self.update_status("Çağrı Aktif", "green")
        self.add_message("Sistem", "Çağrı başlatıldı", "system")
    
    def stop_call(self):
        """Çağrı durdur"""
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self.update_status("Sistem Hazır", "blue")
        self.add_message("Sistem", "Çağrı sonlandırıldı", "system")
    
    def clear_status(self):
        """Durum mesajını temizle"""
        self.update_status("Dinleniyor...", "yellow")

    def notify_speak(self):
        """Konuşma bildirimi"""
        self.update_status("Müşteri Konuşuyor", "yellow")
    
    def _status_update_loop(self):
        """Durum güncelleme döngüsü"""
        while True:
            try:
                # İstatistikleri güncelle
                if gecmis_yoneticisi:
                    stats = gecmis_yoneticisi.istatistikleri_getir()
                    self.root.after(0, lambda: self.update_stats(
                        call_count=stats.get('toplam_gorusme', 0)
                    ))
            except Exception as e:
                print(f"İstatistik güncelleme hatası: {e}")
            
            time.sleep(5)  # 5 saniyede bir güncelle
    
    def _show_gecmis_gorusmeler(self):
        """Geçmiş görüşmeler penceresi"""
        if not gecmis_yoneticisi:
            messagebox.showwarning("Uyarı", "Geçmiş görüşmeler modülü bulunamadı!")
            return
        
        # Yeni pencere oluştur
        gecmis_window = tk.Toplevel(self.root)
        gecmis_window.title("📋 Geçmiş Görüşmeler")
        gecmis_window.geometry("1000x700")
        gecmis_window.configure(bg='#0a0a0a')
        
        # Arama frame
        search_frame = ttk.Frame(gecmis_window, style='Status.TFrame')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(search_frame, text="🔍 Arama:", style='Subtitle.TLabel').pack(side='left')
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side='left', padx=10)
        
        # Treeview
        tree_frame = ttk.Frame(gecmis_window, style='Card.TFrame')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('Tarih', 'Telefon', 'Müşteri', 'Kategori', 'Süre', 'Durum', 'Çözülme')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Scrollbar
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")
        
        # Verileri yükle
        def load_data():
            tree.delete(*tree.get_children())
            gorusmeler = gecmis_yoneticisi.son_gorusmeler_getir(100)
            for gorusme in gorusmeler:
                tarih = datetime.fromisoformat(gorusme["baslangic_zamani"]).strftime("%d.%m.%Y %H:%M")
                tree.insert('', 'end', values=(
                    tarih,
                    gorusme.get('telefon', ''),
                    gorusme.get('musteri_adi', ''),
                    gorusme.get('kategori', 'Bilinmiyor'),
                    f"{gorusme.get('sure', 0):.1f}dk",
                    gorusme.get('durum', ''),
                    gorusme.get('cozulme_durumu', '')
                ))
        
        load_data()
        
        # Arama fonksiyonu
        def search_gorusmeler(*args):
            search_term = search_var.get().lower()
            tree.delete(*tree.get_children())
            gorusmeler = gecmis_yoneticisi.gorusme_ara(search_term)
            for gorusme in gorusmeler:
                tarih = datetime.fromisoformat(gorusme["baslangic_zamani"]).strftime("%d.%m.%Y %H:%M")
                tree.insert('', 'end', values=(
                    tarih,
                    gorusme.get('telefon', ''),
                    gorusme.get('musteri_adi', ''),
                    gorusme.get('kategori', 'Bilinmiyor'),
                    f"{gorusme.get('sure', 0):.1f}dk",
                    gorusme.get('durum', ''),
                    gorusme.get('cozulme_durumu', '')
                ))
        
        search_var.trace('w', search_gorusmeler)
    
    def _show_istatistikler(self):
        """İstatistikler penceresi"""
        if not gecmis_yoneticisi:
            messagebox.showwarning("Uyarı", "Geçmiş görüşmeler modülü bulunamadı!")
            return
        
        # Yeni pencere oluştur
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Çağrı İstatistikleri")
        stats_window.geometry("800x600")
        stats_window.configure(bg='#0a0a0a')
        
        # İstatistikler
        stats = gecmis_yoneticisi.istatistikleri_getir()
        
        stats_frame = ttk.Frame(stats_window, style='Card.TFrame')
        stats_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # İstatistik kartları
        cards = [
            ("📞 Toplam Çağrı", stats.get('toplam_gorusme', 0)),
            ("📅 Bugünkü Çağrı", stats.get('bugun_gorusme', 0)),
            ("🔄 Aktif Çağrı", stats.get('aktif_gorusme', 0)),
            ("📋 En Çok Kategori", stats.get('top_kategori', 'Yok'))
        ]
        
        for i, (title, value) in enumerate(cards):
            card = ttk.Frame(stats_frame, style='Card.TFrame')
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='ew')
            
            ttk.Label(card, text=title, style='Subtitle.TLabel').pack(pady=(10, 5))
            ttk.Label(card, text=str(value), style='Title.TLabel').pack(pady=(0, 10))
        
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
    
    def _show_ayarlar(self):
        """Ayarlar penceresi"""
        messagebox.showinfo("Ayarlar", "Ayarlar penceresi yakında eklenecek!")
    
    def _exit_application(self):
        """Uygulamadan çık"""
        if messagebox.askokcancel("Çıkış", "Uygulamadan çıkmak istediğinizden emin misiniz?"):
            self.root.quit()
    
    def add_system_log(self, log_message: str, log_type: str = "INFO"):
        """Sistem log paneline mesaj ekle"""
        def update_log():
            try:
                # Log formatı
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                # Log tipi renkleri
                color_map = {
                    "INFO": "#58a6ff",
                    "WARNING": "#f85149", 
                    "ERROR": "#ff6b6b",
                    "SUCCESS": "#3fb950",
                    "DEBUG": "#a5a5a5"
                }
                color = color_map.get(log_type, "#c9d1d9")
                
                # Log text widget'ına ekle
                self.log_text.configure(state='normal')
                
                # Timestamp
                self.log_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                
                # Log tipi
                self.log_text.insert(tk.END, f"{log_type}: ", f'log_type_{log_type}')
                
                # Mesaj
                self.log_text.insert(tk.END, f"{log_message}\n", 'message')
                
                # Tag formatları
                self.log_text.tag_configure('timestamp', foreground='#7d8590', font=('Consolas', 8))
                self.log_text.tag_configure(f'log_type_{log_type}', foreground=color, font=('Consolas', 8, 'bold'))
                self.log_text.tag_configure('message', foreground='#c9d1d9', font=('Consolas', 9))
                
                # En alta scroll
                self.log_text.see(tk.END)
                
                # Max 1000 satır tut
                lines = self.log_text.get("1.0", tk.END).count('\n')
                if lines > 1000:
                    self.log_text.delete("1.0", "200.0")
                
                self.log_text.configure(state='disabled')
                
            except Exception as e:
                print(f"Log ekleme hatası: {e}")
        
        # GUI thread'de çalıştır
        if threading.current_thread() == threading.main_thread():
            update_log()
        else:
            self.root.after(0, update_log)
    
    def clear_system_logs(self):
        """Sistem loglarını temizle"""
        try:
            self.log_text.configure(state='normal')
            self.log_text.delete("1.0", tk.END)
            self.log_text.configure(state='disabled')
            self.add_system_log("Loglar temizlendi", "INFO")
        except Exception as e:
            print(f"Log temizleme hatası: {e}")
    
    def setup_log_handler(self):
        """UI log handler'ını kurar"""
        try:
            # Mevcut logger'ı al
            logger = logging.getLogger("CagriMerkezi")
            
            # UI handler'ı oluştur ve ekle
            ui_handler = UILogHandler(self)
            ui_handler.setLevel(logging.INFO)
            
            # Formatter ekle
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
            ui_handler.setFormatter(formatter)
            
            # Logger'a handler'ı ekle
            logger.addHandler(ui_handler)
            
            # İlk log mesajı
            self.add_system_log("Sistem log paneli başlatıldı", "SUCCESS")
            
        except Exception as e:
            print(f"Log handler kurulumu hatası: {e}")

    def run(self):
        """UI'ı çalıştır"""
        self.root.mainloop()

# Eski UI sınıfını koru (geriye uyumluluk için)
class CagriMerkeziUI(UltraModernCagriMerkeziUI):
    pass

class ModernCagriMerkeziUI(UltraModernCagriMerkeziUI):
    pass
