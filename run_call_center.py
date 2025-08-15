#!/usr/bin/env python3
"""
AI Voice Call Center System - Main Launcher Script
This script runs the project in a portable way.

Developed by Trivox Team:
- Serhatcan Ünal, Elif Zeynep Tosun, Meryem Gençali, Ali Buğrahan Budak

Çağrı Merkezi Akıllı Yanıt Sistemi - Ana Başlatma Scripti
Bu script projeyi portable bir şekilde çalıştırır.
"""

import os
import sys
from pathlib import Path

# Proje root dizinini bul ve Python path'ine ekle
def setup_project_path():
    """Proje path'ini ayarlar"""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent
    scripts_dir = project_root / "scripts"
    
    # Scripts dizinini Python path'ine ekle
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    
    return project_root, scripts_dir

def check_dependencies():
    """Gerekli bağımlılıkları kontrol eder"""
    required_packages = [
        'torch',
        'transformers',
        'speech_recognition',
        'gtts',
        'pyaudio',
        'pydub',
        'numpy',
        'sklearn',
        'tqdm'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Eksik bağımlılıklar tespit edildi:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Kurulum için şu komutu çalıştırın:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ Tüm bağımlılıklar mevcut")
    return True

def check_files():
    """Gerekli dosyaları kontrol eder"""
    project_root, scripts_dir = setup_project_path()
    
    required_files = [
        project_root / "data" / "kullanici_faturalar.json",
        project_root / "models" / "berturk_cagri_model" / "config.json",
        scripts_dir / "voice_call_center.py",
        scripts_dir / "call_center_ui.py",
        scripts_dir / "config.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        print("❌ Eksik dosyalar tespit edildi:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Tüm gerekli dosyalar mevcut")
    return True

def main():
    """Ana fonksiyon"""
    print("🎯 Çağrı Merkezi Akıllı Yanıt Sistemi")
    print("=" * 50)
    
    # Path ayarlarını yap
    project_root, scripts_dir = setup_project_path()
    print(f"📁 Proje dizini: {project_root}")
    print(f"📁 Scripts dizini: {scripts_dir}")
    
    # Bağımlılıkları kontrol et
    print("\n🔍 Bağımlılık kontrolü...")
    if not check_dependencies():
        return
    
    # Dosyaları kontrol et
    print("\n🔍 Dosya kontrolü...")
    if not check_files():
        return
    
    # Config'i import et ve gerekli dizinleri oluştur
    try:
        sys.path.insert(0, str(scripts_dir))
        from config import create_directories, check_required_files
        
        print("\n📂 Dizinler oluşturuluyor...")
        create_directories()
        
        print("\n🔍 Gerekli dosyalar kontrol ediliyor...")
        if not check_required_files():
            print("⚠️  Bazı gerekli dosyalar eksik olabilir, ancak devam ediliyor...")
        
    except ImportError as e:
        print(f"⚠️  Config dosyası yüklenemedi: {e}")
        print("Basit modda devam ediliyor...")
    
    # Ana uygulamayı başlat
    print("\n🚀 Çağrı merkezi başlatılıyor...")
    try:
        # Sesli çağrı merkezi modülünü import et
        from voice_call_center import SesliCagriMerkezi
        from call_center_ui import UltraModernCagriMerkeziUI
        
        # UI ve çağrı merkezi nesnelerini oluştur
        ui = UltraModernCagriMerkeziUI()
        cagri_merkezi = SesliCagriMerkezi(ui=ui)
        
        # Çağrı merkezini ayrı thread'de başlat
        import threading
        threading.Thread(target=cagri_merkezi.cagri_merkezi_baslat, daemon=True).start()
        
        # UI'yi çalıştır
        ui.run()
        
    except Exception as e:
        print(f"❌ Uygulama başlatılamadı: {e}")
        print("\n🔧 Hata ayıklama bilgileri:")
        print(f"   Python sürümü: {sys.version}")
        print(f"   Çalışma dizini: {os.getcwd()}")
        print(f"   Python path: {sys.path[:3]}...")

if __name__ == "__main__":
    main()
