"""
Ağ Bağlantı Testi
Google servislerine bağlantıyı test eder ve sorunları teşhis eder.
"""

import socket
import requests
import time
from urllib.parse import urlparse
import subprocess
import platform

def test_basic_connectivity():
    """Temel internet bağlantısını test eder"""
    print("🌐 Temel internet bağlantısı test ediliyor...")
    
    # DNS çözümleme testi
    try:
        socket.gethostbyname("google.com")
        print("✅ DNS çözümleme başarılı")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS çözümleme hatası: {e}")
        return False

def test_google_services():
    """Google servislerine bağlantıyı test eder"""
    print("\n🔍 Google servisleri test ediliyor...")
    
    services = {
        "Google Ana Sayfa": "https://www.google.com",
        "Google Speech API": "https://speech.googleapis.com",
        "Google Translate": "https://translate.googleapis.com",
        "gTTS Servisi": "https://translate.google.com"
    }
    
    results = {}
    
    for service_name, url in services.items():
        try:
            print(f"  {service_name} test ediliyor...")
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"  ✅ {service_name}: Başarılı")
                results[service_name] = True
            else:
                print(f"  ⚠️ {service_name}: HTTP {response.status_code}")
                results[service_name] = False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {service_name}: {e}")
            results[service_name] = False
    
    return results

def test_specific_ports():
    """Belirli portları test eder"""
    print("\n🔌 Port bağlantıları test ediliyor...")
    
    ports = {
        "HTTP (80)": 80,
        "HTTPS (443)": 443,
        "DNS (53)": 53
    }
    
    for port_name, port in ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(("8.8.8.8", port))
            sock.close()
            
            if result == 0:
                print(f"  ✅ {port_name}: Açık")
            else:
                print(f"  ❌ {port_name}: Kapalı")
        except Exception as e:
            print(f"  ❌ {port_name}: Hata - {e}")

def test_dns_servers():
    """DNS sunucularını test eder"""
    print("\n📡 DNS sunucuları test ediliyor...")
    
    dns_servers = [
        ("Google DNS (8.8.8.8)", "8.8.8.8"),
        ("Google DNS (8.8.4.4)", "8.8.4.4"),
        ("Cloudflare DNS (1.1.1.1)", "1.1.1.1"),
        ("OpenDNS (208.67.222.222)", "208.67.222.222")
    ]
    
    for dns_name, dns_ip in dns_servers:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((dns_ip, 53))
            sock.close()
            
            if result == 0:
                print(f"  ✅ {dns_name}: Erişilebilir")
            else:
                print(f"  ❌ {dns_name}: Erişilemez")
        except Exception as e:
            print(f"  ❌ {dns_name}: Hata - {e}")

def test_proxy_settings():
    """Proxy ayarlarını kontrol eder"""
    print("\n🔧 Proxy ayarları kontrol ediliyor...")
    
    # Sistem proxy ayarlarını kontrol et
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"  ⚠️ {var}: {value}")
        else:
            print(f"  ✅ {var}: Ayarlanmamış")

def test_firewall():
    """Güvenlik duvarı durumunu kontrol eder"""
    print("\n🛡️ Güvenlik duvarı kontrol ediliyor...")
    
    system = platform.system()
    
    if system == "Windows":
        try:
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                print("  ✅ Windows Güvenlik Duvarı durumu alındı")
                # Basit kontrol
                if "ON" in result.stdout:
                    print("  ⚠️ Güvenlik duvarı aktif - Google servisleri engellenmiş olabilir")
                else:
                    print("  ✅ Güvenlik duvarı pasif")
            else:
                print("  ❌ Güvenlik duvarı durumu alınamadı")
        except Exception as e:
            print(f"  ❌ Güvenlik duvarı kontrol hatası: {e}")
    else:
        print("  ℹ️ Windows dışı sistem - Güvenlik duvarı kontrolü atlandı")

def run_comprehensive_test():
    """Kapsamlı ağ testi çalıştırır"""
    print("🚀 Kapsamlı Ağ Bağlantı Testi Başlatılıyor...")
    print("=" * 50)
    
    # Temel bağlantı testi
    basic_ok = test_basic_connectivity()
    
    if not basic_ok:
        print("\n❌ Temel internet bağlantısı yok!")
        print("Çözüm önerileri:")
        print("1. İnternet bağlantınızı kontrol edin")
        print("2. Modem/router'ı yeniden başlatın")
        print("3. DNS ayarlarını kontrol edin")
        return False
    
    # Diğer testler
    test_google_services()
    test_specific_ports()
    test_dns_servers()
    test_proxy_settings()
    test_firewall()
    
    print("\n" + "=" * 50)
    print("📋 Test Sonuçları:")
    print("✅ Temel internet bağlantısı mevcut")
    print("⚠️ Google servislerine erişim sorunları olabilir")
    print("\n🔧 Çözüm önerileri:")
    print("1. VPN kullanıyorsanız kapatın")
    print("2. Güvenlik duvarı ayarlarını kontrol edin")
    print("3. DNS ayarlarını 8.8.8.8 ve 8.8.4.4 olarak değiştirin")
    print("4. Proxy ayarlarını kontrol edin")
    print("5. Antivirüs yazılımının Google servislerini engellemediğinden emin olun")
    
    return True

if __name__ == "__main__":
    import os
    run_comprehensive_test()
