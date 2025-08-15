"""
Çağrı Merkezi Logging Konfigürasyonu
Bu dosya uygulama loglarını yönetir ve hata takibi sağlar.
"""

import logging
import os
from pathlib import Path
from datetime import datetime
import sys

def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Logging sistemini kurar
    
    Args:
        log_level: Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Log dosyası yolu (None ise otomatik oluşturulur)
    """
    
    # Proje root dizinini bul
    current_file = Path(__file__).resolve()
    if current_file.parent.name == 'scripts':
        project_root = current_file.parent.parent
    else:
        project_root = current_file.parent
    
    # Log dizinini oluştur
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Log dosyası adını belirle
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"cagri_merkezi_{timestamp}.log"
    
    # Logger'ı yapılandır
    logger = logging.getLogger('CagriMerkezi')
    logger.setLevel(log_level)
    
    # Eğer handler'lar zaten eklenmişse, tekrar ekleme
    if logger.handlers:
        return logger
    
    # Dosya handler'ı
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    
    # Konsol handler'ı
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Format belirle
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Handler'ları ekle
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name='CagriMerkezi'):
    """
    Logger instance'ı döndürür
    
    Args:
        name: Logger adı
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

# Özel log fonksiyonları
def log_network_error(logger, error, context=""):
    """Ağ hatalarını loglar"""
    logger.error(f"Ağ Hatası {context}: {error}")
    logger.debug(f"Hata detayı: {type(error).__name__}: {str(error)}")

def log_audio_error(logger, error, context=""):
    """Ses işleme hatalarını loglar"""
    logger.error(f"Ses Hatası {context}: {error}")
    logger.debug(f"Hata detayı: {type(error).__name__}: {str(error)}")

def log_model_error(logger, error, context=""):
    """Model hatalarını loglar"""
    logger.error(f"Model Hatası {context}: {error}")
    logger.debug(f"Hata detayı: {type(error).__name__}: {str(error)}")

def log_ui_error(logger, error, context=""):
    """UI hatalarını loglar"""
    logger.error(f"UI Hatası {context}: {error}")
    logger.debug(f"Hata detayı: {type(error).__name__}: {str(error)}")

def log_performance(logger, operation, duration, context=""):
    """Performans metriklerini loglar"""
    logger.info(f"Performans {context}: {operation} - {duration:.2f}s")

def log_user_interaction(logger, action, details=""):
    """Kullanıcı etkileşimlerini loglar"""
    logger.info(f"Kullanıcı Etkileşimi: {action} - {details}")

def log_system_status(logger, component, status, details=""):
    """Sistem durumunu loglar"""
    logger.info(f"Sistem Durumu: {component} - {status} - {details}")

# Varsayılan logger'ı oluştur
default_logger = setup_logging(logging.INFO)
