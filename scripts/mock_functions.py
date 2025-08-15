"""
Mock Fonksiyonlar - Teknik Şartname Gereksinimleri
Telekom çağrı merkezi için sahte API fonksiyonları
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

class MockTelecomSystem:
    """Telekom sistemi mock fonksiyonları"""
    
    def __init__(self):
        self.customers = {
            "5375944025": {
                "name": "Elif Zeynep",
                "surname": "TOSUN",
                "current_package": "SuperNet 50",
                "contract_end_date": "2025-12-31",
                "payment_status": "Odendi",
                "balance": 150.0,
                "phone_number": "5375944025",
                "tc_last_digits": "46",
                "sim_pin": "1234"
            },
            "5551234567": {
                "name": "Ahmet",
                "surname": "YILMAZ",
                "current_package": "Ekonomik Paket",
                "contract_end_date": "2025-06-15",
                "payment_status": "Gecikmis",
                "balance": -25.0,
                "phone_number": "5551234567",
                "tc_last_digits": "89",
                "sim_pin": "5678"
            }
        }
        
        self.packages = [
            {
                "id": "PN1",
                "name": "MegaPaket 100",
                "price": 150.0,
                "details": "100Mbps internet, limitsiz konuşma, 10GB mobil",
                "speed": "100 Mbps",
                "mobile_data": "10 GB"
            },
            {
                "id": "PN2", 
                "name": "Ekonomik Paket",
                "price": 80.0,
                "details": "25Mbps internet, 1000 dakika konuşma, 5GB mobil",
                "speed": "25 Mbps",
                "mobile_data": "5 GB"
            },
            {
                "id": "PN3",
                "name": "Premium Paket",
                "price": 200.0,
                "details": "500Mbps internet, limitsiz konuşma, 50GB mobil",
                "speed": "500 Mbps",
                "mobile_data": "50 GB"
            }
        ]
        
        self.bills = {
            "5375944025": [
                {"month": "2025-01", "amount": 150.0, "status": "Odendi"},
                {"month": "2025-02", "amount": 150.0, "status": "Odendi"},
                {"month": "2025-03", "amount": 150.0, "status": "Beklemede"}
            ],
            "5551234567": [
                {"month": "2025-01", "amount": 80.0, "status": "Gecikmis"},
                {"month": "2025-02", "amount": 80.0, "status": "Gecikmis"},
                {"month": "2025-03", "amount": 80.0, "status": "Beklemede"}
            ]
        }

    def getUserInfo(self, user_id: str) -> Dict:
        """
        Kullanıcı bilgilerini getir
        Teknik şartname gereksinimi: getUserInfo(user_id)
        """
        try:
            if user_id in self.customers:
                customer = self.customers[user_id].copy()
                return {
                    "success": True,
                    "data": customer,
                    "message": "Kullanıcı bilgileri başarıyla getirildi"
                }
            else:
                return {
                    "success": False,
                    "error": "Kullanıcı bulunamadı",
                    "message": f"{user_id} numaralı kullanıcı sistemde kayıtlı değil"
                }
        except Exception as e:
            return {
                "success": False,
                "error": "Sistem hatası",
                "message": f"Kullanıcı bilgileri alınırken hata oluştu: {str(e)}"
            }

    def getAvailablePackages(self, user_id: str) -> Dict:
        """
        Kullanıcıya uygun paketleri listele
        Teknik şartname gereksinimi: getAvailablePackages(user_id)
        """
        try:
            if user_id not in self.customers:
                return {
                    "success": False,
                    "error": "Kullanıcı bulunamadı",
                    "packages": []
                }
            
            customer = self.customers[user_id]
            available_packages = []
            
            # Kullanıcının mevcut durumuna göre paket filtreleme
            for package in self.packages:
                # Gecikmiş ödemesi olan kullanıcılar için premium paketleri kısıtla
                if customer["payment_status"] == "Gecikmis" and package["price"] > 150:
                    continue
                    
                available_packages.append(package)
            
            return {
                "success": True,
                "packages": available_packages,
                "message": f"{len(available_packages)} adet uygun paket bulundu"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "Sistem hatası",
                "packages": [],
                "message": f"Paket listesi alınırken hata oluştu: {str(e)}"
            }

    def initiatePackageChange(self, user_id: str, package_id: str) -> Dict:
        """
        Paket değişikliği başlat
        Teknik şartname gereksinimi: initiatePackageChange(user_id, package_id)
        """
        try:
            if user_id not in self.customers:
                return {
                    "success": False,
                    "error": "Kullanıcı bulunamadı",
                    "message": "Geçersiz kullanıcı ID'si"
                }
            
            # Paket ID'sini kontrol et
            package = None
            for pkg in self.packages:
                if pkg["id"] == package_id:
                    package = pkg
                    break
            
            if not package:
                return {
                    "success": False,
                    "error": "Paket bulunamadı",
                    "message": "Geçersiz paket ID'si"
                }
            
            customer = self.customers[user_id]
            
            # Gecikmiş ödemesi olan kullanıcılar için kısıtlama
            if customer["payment_status"] == "Gecikmis":
                return {
                    "success": False,
                    "error": "Ödeme gecikmesi",
                    "message": "Gecikmiş ödemeniz nedeniyle paket değişikliği yapamazsınız. Lütfen önce borcunuzu ödeyin."
                }
            
            # Sözleşme bitiş tarihini kontrol et
            contract_end = datetime.strptime(customer["contract_end_date"], "%Y-%m-%d")
            if contract_end > datetime.now() + timedelta(days=30):
                return {
                    "success": False,
                    "error": "Sözleşme kısıtlaması",
                    "message": "Sözleşmeniz henüz bitmemiş. Paket değişikliği için sözleşme bitiş tarihini bekleyin."
                }
            
            # Başarılı paket değişikliği
            old_package = customer["current_package"]
            customer["current_package"] = package["name"]
            
            return {
                "success": True,
                "message": f"Paket değişikliği başarıyla başlatıldı. {old_package} paketinden {package['name']} paketine geçiş 24 saat içinde aktifleşecektir.",
                "old_package": old_package,
                "new_package": package["name"],
                "activation_time": "24 saat"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "Sistem hatası",
                "message": f"Paket değişikliği sırasında hata oluştu: {str(e)}"
            }

    def getBillingInfo(self, user_id: str) -> Dict:
        """
        Fatura bilgilerini getir
        """
        try:
            if user_id not in self.bills:
                return {
                    "success": False,
                    "error": "Fatura bilgisi bulunamadı",
                    "bills": []
                }
            
            bills = self.bills[user_id]
            total_owed = sum(bill["amount"] for bill in bills if bill["status"] == "Gecikmis")
            
            return {
                "success": True,
                "bills": bills,
                "total_owed": total_owed,
                "message": f"Son {len(bills)} ayın fatura bilgileri getirildi"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "Sistem hatası",
                "bills": [],
                "message": f"Fatura bilgileri alınırken hata oluştu: {str(e)}"
            }

    def validateCustomer(self, phone_number: str, tc_last_digits: str, sim_pin: str) -> Dict:
        """
        Müşteri doğrulama
        """
        try:
            if phone_number not in self.customers:
                return {
                    "success": False,
                    "error": "Müşteri bulunamadı",
                    "message": "Telefon numarası sistemde kayıtlı değil"
                }
            
            customer = self.customers[phone_number]
            
            if customer["tc_last_digits"] != tc_last_digits:
                return {
                    "success": False,
                    "error": "TC kimlik hatası",
                    "message": "TC kimlik numarasının son iki hanesi hatalı"
                }
            
            if customer["sim_pin"] != sim_pin:
                return {
                    "success": False,
                    "error": "SIM PIN hatası",
                    "message": "SIM kart şifresi hatalı"
                }
            
            return {
                "success": True,
                "message": "Müşteri doğrulaması başarılı",
                "customer_name": f"{customer['name']} {customer['surname']}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "Doğrulama hatası",
                "message": f"Müşteri doğrulaması sırasında hata oluştu: {str(e)}"
            }

# Global mock sistem instance'ı
mock_system = MockTelecomSystem()

# Teknik şartname gereksinimlerine uygun fonksiyonlar
def getUserInfo(user_id: str) -> Dict:
    """Teknik şartname gereksinimi: getUserInfo(user_id)"""
    return mock_system.getUserInfo(user_id)

def getAvailablePackages(user_id: str) -> Dict:
    """Teknik şartname gereksinimi: getAvailablePackages(user_id)"""
    return mock_system.getAvailablePackages(user_id)

def initiatePackageChange(user_id: str, package_id: str) -> Dict:
    """Teknik şartname gereksinimi: initiatePackageChange(user_id, package_id)"""
    return mock_system.initiatePackageChange(user_id, package_id)

def getBillingInfo(user_id: str) -> Dict:
    """Ek fonksiyon: Fatura bilgileri"""
    return mock_system.getBillingInfo(user_id)

def validateCustomer(phone_number: str, tc_last_digits: str, sim_pin: str) -> Dict:
    """Ek fonksiyon: Müşteri doğrulama"""
    return mock_system.validateCustomer(phone_number, tc_last_digits, sim_pin)
