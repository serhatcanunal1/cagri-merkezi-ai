"""
Çağrı Merkezi Projesi Konfigürasyon Dosyası
Bu dosya proje ayarlarını merkezi olarak yönetir.
"""

import os
from pathlib import Path

# Proje root dizinini dinamik olarak bul
def get_project_root():
    """Proje root dizinini bulur"""
    current_file = Path(__file__).resolve()
    # scripts/ klasöründeyse bir üst dizine çık
    if current_file.parent.name == 'scripts':
        return current_file.parent.parent
    # Eğer doğrudan root'taysa
    return current_file.parent

# Proje root path'ini global olarak tanımla
PROJECT_ROOT = get_project_root()

# Veri dosyaları
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

# Dosya yolları
KULLANICI_FATURALAR_FILE = DATA_DIR / "kullanici_faturalar.json"
TRAIN_BERTURK_FILE = DATA_DIR / "train_berturk.jsonl"
SIKAYETLER_FILE = DATA_DIR / "sikayetler.csv"
SIKAYETLER_TEMIZ_FILE = DATA_DIR / "sikayetler_temiz.csv"

# Model yolları
BERTURK_CAGRI_MODEL_DIR = MODELS_DIR / "berturk_cagri_model"
BERTURK_FINETUNED_DIR = MODELS_DIR / "berturk_finetuned"

# FFmpeg ayarları
def setup_ffmpeg_paths():
    """FFmpeg path'lerini ayarlar"""
    if os.name == 'nt':  # Windows
        # Önce scoop ile kurulu olup olmadığını kontrol et
        user_profile = os.environ.get('USERPROFILE')
        scoop_ffmpeg = os.path.join(user_profile, 'scoop', 'shims', 'ffmpeg.exe')
        scoop_ffprobe = os.path.join(user_profile, 'scoop', 'shims', 'ffprobe.exe')
        
        # Eğer scoop ile kuruluysa kullan
        if os.path.exists(scoop_ffmpeg):
            try:
                from pydub import AudioSegment
                AudioSegment.converter = scoop_ffmpeg
                AudioSegment.ffmpeg = scoop_ffmpeg
                AudioSegment.ffprobe = scoop_ffprobe
                os.environ['PATH'] += os.pathsep + os.path.dirname(scoop_ffmpeg)
                os.environ['FFMPEG_BINARY'] = scoop_ffmpeg
                return True
            except ImportError:
                pass
        else:
            # Sistem PATH'inde ffmpeg var mı kontrol et
            try:
                import subprocess
                subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                # FFmpeg PATH'de bulundu, ek ayar gerekmez
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Uyarı: FFmpeg bulunamadı. Ses işleme özellikleri çalışmayabilir.")
                return False
    return True

# Kategori tanımları
KATEGORILER = {
    0: 'Fatura İtirazı',
    1: 'Paket Kalan Hak Sorgulama',
    2: 'Borç/Ödeme Sorgulama',
    3: 'İptal Talebi',
    4: 'Yeni Paket/Kampanya Sorgulama',
    5: 'Teknik Arıza',
    6: 'Sim Kart Şifre'
}

# Ses tanıma ayarları
SPEECH_RECOGNITION_CONFIG = {
    'language': 'tr-TR',
    'timeout': 20,
    'phrase_time_limit': 10
}

# Model ayarları
MODEL_CONFIG = {
    'max_length': 64,
    'batch_size': 8,
    'learning_rate': 5e-5,
    'num_epochs': 10
}

# Dosya varlık kontrolü
def check_required_files():
    """Gerekli dosyaların varlığını kontrol eder"""
    required_files = [
        KULLANICI_FATURALAR_FILE,
        BERTURK_CAGRI_MODEL_DIR
    ]
    
    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        print("Uyarı: Aşağıdaki gerekli dosyalar bulunamadı:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    return True

# Dizinleri oluştur
def create_directories():
    """Gerekli dizinleri oluşturur"""
    directories = [DATA_DIR, MODELS_DIR, BERTURK_CAGRI_MODEL_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
