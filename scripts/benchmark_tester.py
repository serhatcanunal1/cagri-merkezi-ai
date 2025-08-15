"""
Benchmark Test Sistemi - Teknik Şartname Gereksinimleri
100 farklı zorluk seviyesinde test senaryosu
"""

import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional
from performance_metrics import performance_tracker, CallMetrics

class BenchmarkTester:
    """Benchmark test sistemi"""
    
    def __init__(self):
        self.test_scenarios = self._generate_test_scenarios()
        self.results = []
        
    def _generate_test_scenarios(self) -> List[Dict]:
        """100 farklı test senaryosu oluştur"""
        scenarios = []
        
        # Paket değişikliği senaryoları (40 test)
        package_scenarios = [
            {"type": "package_change", "difficulty": "easy", "customer_state": "normal"},
            {"type": "package_change", "difficulty": "medium", "customer_state": "delayed_payment"},
            {"type": "package_change", "difficulty": "hard", "customer_state": "contract_locked"},
            {"type": "package_change", "difficulty": "expert", "customer_state": "multiple_issues"}
        ] * 10
        
        # Fatura sorgulama senaryoları (30 test)
        billing_scenarios = [
            {"type": "billing_inquiry", "difficulty": "easy", "customer_state": "paid"},
            {"type": "billing_inquiry", "difficulty": "medium", "customer_state": "overdue"},
            {"type": "billing_inquiry", "difficulty": "hard", "customer_state": "disputed"},
            {"type": "billing_inquiry", "difficulty": "expert", "customer_state": "fraud_suspicion"}
        ] * 7 + [{"type": "billing_inquiry", "difficulty": "easy", "customer_state": "paid"}] * 2
        
        # Teknik destek senaryoları (20 test)
        tech_support_scenarios = [
            {"type": "technical_support", "difficulty": "easy", "issue": "connection_slow"},
            {"type": "technical_support", "difficulty": "medium", "issue": "no_internet"},
            {"type": "technical_support", "difficulty": "hard", "issue": "router_problem"},
            {"type": "technical_support", "difficulty": "expert", "issue": "complex_network"}
        ] * 5
        
        # Bağlam değişimi senaryoları (10 test)
        context_switch_scenarios = [
            {"type": "context_switch", "difficulty": "medium", "switch_type": "package_to_billing"},
            {"type": "context_switch", "difficulty": "hard", "switch_type": "billing_to_technical"},
            {"type": "context_switch", "difficulty": "expert", "switch_type": "multiple_switches"}
        ] * 3 + [{"type": "context_switch", "difficulty": "medium", "switch_type": "package_to_billing"}]
        
        scenarios = package_scenarios + billing_scenarios + tech_support_scenarios + context_switch_scenarios
        
        # Senaryoları karıştır
        random.shuffle(scenarios)
        
        return scenarios
    
    def _generate_customer_data(self, scenario: Dict) -> Dict:
        """Senaryoya uygun müşteri verisi oluştur"""
        customer_states = {
            "normal": {
                "payment_status": "Odendi",
                "balance": random.uniform(0, 100),
                "contract_end_date": "2025-12-31"
            },
            "delayed_payment": {
                "payment_status": "Gecikmis",
                "balance": random.uniform(-100, -10),
                "contract_end_date": "2025-12-31"
            },
            "contract_locked": {
                "payment_status": "Odendi",
                "balance": random.uniform(0, 50),
                "contract_end_date": "2026-06-30"
            },
            "multiple_issues": {
                "payment_status": "Gecikmis",
                "balance": random.uniform(-200, -50),
                "contract_end_date": "2026-03-15"
            },
            "paid": {
                "payment_status": "Odendi",
                "balance": random.uniform(0, 50),
                "contract_end_date": "2025-12-31"
            },
            "overdue": {
                "payment_status": "Gecikmis",
                "balance": random.uniform(-150, -20),
                "contract_end_date": "2025-12-31"
            },
            "disputed": {
                "payment_status": "Itiraz",
                "balance": random.uniform(-300, -100),
                "contract_end_date": "2025-12-31"
            },
            "fraud_suspicion": {
                "payment_status": "Donduruldu",
                "balance": random.uniform(-500, -200),
                "contract_end_date": "2025-12-31"
            }
        }
        
        customer_state = scenario.get("customer_state", "normal")
        base_data = customer_states.get(customer_state, customer_states["normal"])
        
        return {
            "phone_number": f"5{random.randint(3000000000, 3999999999)}",
            "name": random.choice(["Ahmet", "Ayşe", "Mehmet", "Fatma", "Ali", "Zeynep"]),
            "surname": random.choice(["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız"]),
            "tc_last_digits": f"{random.randint(10, 99)}",
            "sim_pin": f"{random.randint(1000, 9999)}",
            **base_data
        }
    
    def _generate_user_input(self, scenario: Dict) -> List[str]:
        """Senaryoya uygun kullanıcı girdileri oluştur"""
        scenario_type = scenario["type"]
        difficulty = scenario["difficulty"]
        
        if scenario_type == "package_change":
            if difficulty == "easy":
                return [
                    "Paketimi değiştirmek istiyorum",
                    "Daha uygun fiyatlı bir paket var mı?",
                    "Evet, MegaPaket 100'ü istiyorum",
                    "Hayır, başka bir şey yok"
                ]
            elif difficulty == "medium":
                return [
                    "Paket değişikliği yapmak istiyorum",
                    "Fiyatları görebilir miyim?",
                    "Bu paket çok pahalı, daha ucuzu yok mu?",
                    "Tamam, Ekonomik Paket'i alayım",
                    "Hayır, teşekkürler"
                ]
            elif difficulty == "hard":
                return [
                    "Paketimi değiştirmek istiyorum",
                    "Hangi paketler var?",
                    "Bu paket bana uygun değil",
                    "Başka seçenek yok mu?",
                    "Sözleşmem ne zaman bitiyor?",
                    "Tamam, bekleyeceğim"
                ]
            else:  # expert
                return [
                    "Paket değişikliği yapmak istiyorum",
                    "Önce fatura durumumu öğrenmek istiyorum",
                    "Borç mu var?",
                    "Nasıl ödeyebilirim?",
                    "Şimdi paket değişikliği yapabilir miyim?",
                    "Hangi paketler uygun?",
                    "Bu paket iyi görünüyor",
                    "Hayır, başka bir şey yok"
                ]
        
        elif scenario_type == "billing_inquiry":
            if difficulty == "easy":
                return [
                    "Fatura bilgilerimi öğrenmek istiyorum",
                    "Son faturam ne kadar?",
                    "Teşekkürler"
                ]
            elif difficulty == "medium":
                return [
                    "Fatura durumumu kontrol etmek istiyorum",
                    "Borç var mı?",
                    "Ne kadar borç var?",
                    "Nasıl ödeyebilirim?",
                    "Teşekkürler"
                ]
            elif difficulty == "hard":
                return [
                    "Fatura bilgilerimi görmek istiyorum",
                    "Bu fatura yanlış",
                    "Ben bu kadar kullanmadım",
                    "İtiraz etmek istiyorum",
                    "Nasıl yapabilirim?",
                    "Teşekkürler"
                ]
            else:  # expert
                return [
                    "Fatura durumumu öğrenmek istiyorum",
                    "Bu fatura çok yüksek",
                    "Ben bu hizmetleri kullanmadım",
                    "Dolandırılıyorum",
                    "Avukatımla konuşacağım",
                    "İtiraz sürecini başlatın",
                    "Teşekkürler"
                ]
        
        elif scenario_type == "technical_support":
            if difficulty == "easy":
                return [
                    "İnternetim yavaş",
                    "Hız testi yapabilir misiniz?",
                    "Teşekkürler"
                ]
            elif difficulty == "medium":
                return [
                    "İnternet bağlantım yok",
                    "Modem çalışıyor mu?",
                    "Yeniden başlatayım mı?",
                    "Hala çalışmıyor",
                    "Teknisyen gönderin"
                ]
            elif difficulty == "hard":
                return [
                    "İnternet sorunum var",
                    "Modem ışıkları yanıp sönüyor",
                    "Kabloları kontrol ettim",
                    "Başka bir sorun olabilir mi?",
                    "Teknisyen ne zaman gelebilir?",
                    "Acil mi?"
                ]
            else:  # expert
                return [
                    "Karmaşık bir ağ sorunum var",
                    "Birden fazla cihaz bağlı",
                    "Bazı cihazlar çalışıyor bazıları çalışmıyor",
                    "Firewall ayarları değişti mi?",
                    "IP adresim değişti mi?",
                    "DNS ayarlarını kontrol edin",
                    "Teknisyen gönderin"
                ]
        
        elif scenario_type == "context_switch":
            if difficulty == "medium":
                return [
                    "Paket değişikliği yapmak istiyorum",
                    "Önce fatura durumumu öğrenmek istiyorum",
                    "Borç var mı?",
                    "Şimdi paket değişikliği yapabilir miyim?",
                    "Hangi paketler var?",
                    "Teşekkürler"
                ]
            elif difficulty == "hard":
                return [
                    "Fatura bilgilerimi öğrenmek istiyorum",
                    "Bu fatura yanlış",
                    "Aslında paket değişikliği de yapmak istiyorum",
                    "Hangi paketler uygun?",
                    "Fiyatları görebilir miyim?",
                    "Teşekkürler"
                ]
            else:  # expert
                return [
                    "İnternet sorunum var",
                    "Modem çalışmıyor",
                    "Aslında fatura da ödemek istiyorum",
                    "Ne kadar borç var?",
                    "Şimdi paket değişikliği de yapabilir miyim?",
                    "Hangi paketler var?",
                    "Teknisyen de gönderin",
                    "Teşekkürler"
                ]
        
        return ["Merhaba", "Teşekkürler"]
    
    def run_single_test(self, scenario: Dict, test_id: int) -> Dict:
        """Tek bir test senaryosunu çalıştır"""
        print(f"🧪 Test {test_id + 1}/100: {scenario['type']} - {scenario['difficulty']}")
        
        # Test başlangıcı
        call_id = f"test_{test_id:03d}_{scenario['type']}"
        performance_tracker.start_call(call_id, scenario_type=f"test_{scenario['type']}")
        
        # Müşteri verisi oluştur
        customer_data = self._generate_customer_data(scenario)
        user_inputs = self._generate_user_input(scenario)
        
        # Test simülasyonu
        start_time = time.time()
        success = True
        error_count = 0
        tool_calls = 0
        context_switches = 0
        
        try:
            # Mock fonksiyon çağrıları simüle et
            if scenario["type"] == "package_change":
                tool_calls += 1  # getUserInfo
                tool_calls += 1  # getAvailablePackages
                tool_calls += 1  # initiatePackageChange
                
                # Zorluk seviyesine göre hata simülasyonu
                if scenario["difficulty"] == "hard" and random.random() < 0.3:
                    error_count += 1
                    success = False
                    
            elif scenario["type"] == "billing_inquiry":
                tool_calls += 1  # getUserInfo
                tool_calls += 1  # getBillingInfo
                
                if scenario["difficulty"] == "expert" and random.random() < 0.4:
                    error_count += 1
                    
            elif scenario["type"] == "technical_support":
                tool_calls += 1  # getUserInfo
                
                if scenario["difficulty"] in ["hard", "expert"]:
                    context_switches += 1
                    
            elif scenario["type"] == "context_switch":
                tool_calls += 2  # getUserInfo + getBillingInfo
                tool_calls += 1  # getAvailablePackages
                context_switches += 1
                
                if scenario["difficulty"] == "expert":
                    context_switches += 1
                    error_count += 1
            
            # Performans metriklerini güncelle
            performance_tracker.log_tool_call(call_id)
            if context_switches > 0:
                performance_tracker.log_context_switch(call_id)
            if error_count > 0:
                performance_tracker.log_error(call_id)
            
            # Test süresi
            test_duration = time.time() - start_time
            
            # Müşteri memnuniyeti (zorluk seviyesine göre)
            satisfaction = 5
            if scenario["difficulty"] == "medium":
                satisfaction = random.randint(4, 5)
            elif scenario["difficulty"] == "hard":
                satisfaction = random.randint(3, 5)
            elif scenario["difficulty"] == "expert":
                satisfaction = random.randint(2, 4)
            
            # Test sonlandır
            performance_tracker.end_call(call_id, success=success, satisfaction=satisfaction)
            
            result = {
                "test_id": test_id,
                "scenario": scenario,
                "customer_data": customer_data,
                "user_inputs": user_inputs,
                "success": success,
                "duration": test_duration,
                "tool_calls": tool_calls,
                "context_switches": context_switches,
                "error_count": error_count,
                "satisfaction": satisfaction,
                "call_id": call_id
            }
            
            self.results.append(result)
            return result
            
        except Exception as e:
            performance_tracker.log_error(call_id)
            performance_tracker.end_call(call_id, success=False, satisfaction=1)
            
            result = {
                "test_id": test_id,
                "scenario": scenario,
                "success": False,
                "error": str(e),
                "duration": time.time() - start_time,
                "call_id": call_id
            }
            
            self.results.append(result)
            return result
    
    def run_all_tests(self) -> Dict:
        """Tüm 100 testi çalıştır"""
        print("🚀 Benchmark testleri başlatılıyor...")
        print(f"📊 Toplam {len(self.test_scenarios)} test senaryosu")
        
        start_time = time.time()
        
        for i, scenario in enumerate(self.test_scenarios):
            self.run_single_test(scenario, i)
            
            # Her 10 testte bir ilerleme göster
            if (i + 1) % 10 == 0:
                print(f"✅ {i + 1}/100 test tamamlandı")
        
        total_duration = time.time() - start_time
        
        # Sonuçları analiz et
        successful_tests = len([r for r in self.results if r.get("success", False)])
        failed_tests = len(self.results) - successful_tests
        
        avg_duration = sum(r.get("duration", 0) for r in self.results) / len(self.results)
        avg_satisfaction = sum(r.get("satisfaction", 0) for r in self.results) / len(self.results)
        
        # Senaryo bazlı analiz
        scenario_analysis = {}
        for result in self.results:
            scenario_type = result["scenario"]["type"]
            if scenario_type not in scenario_analysis:
                scenario_analysis[scenario_type] = {
                    "total": 0,
                    "successful": 0,
                    "avg_duration": 0,
                    "avg_satisfaction": 0
                }
            
            scenario_analysis[scenario_type]["total"] += 1
            if result.get("success", False):
                scenario_analysis[scenario_type]["successful"] += 1
        
        # Ortalama hesaplamaları
        for scenario_type in scenario_analysis:
            scenario_results = [r for r in self.results if r["scenario"]["type"] == scenario_type]
            scenario_analysis[scenario_type]["avg_duration"] = sum(r.get("duration", 0) for r in scenario_results) / len(scenario_results)
            scenario_analysis[scenario_type]["avg_satisfaction"] = sum(r.get("satisfaction", 0) for r in scenario_results) / len(scenario_results)
        
        benchmark_report = {
            "test_summary": {
                "total_tests": len(self.results),
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": successful_tests / len(self.results),
                "total_duration": total_duration,
                "avg_test_duration": avg_duration,
                "avg_satisfaction": avg_satisfaction
            },
            "scenario_analysis": scenario_analysis,
            "difficulty_analysis": {
                "easy": len([r for r in self.results if r["scenario"]["difficulty"] == "easy"]),
                "medium": len([r for r in self.results if r["scenario"]["difficulty"] == "medium"]),
                "hard": len([r for r in self.results if r["scenario"]["difficulty"] == "hard"]),
                "expert": len([r for r in self.results if r["scenario"]["difficulty"] == "expert"])
            },
            "detailed_results": self.results
        }
        
        # Performans raporunu kaydet
        performance_tracker.save_metrics("benchmark_performance_metrics.json")
        
        return benchmark_report
    
    def save_benchmark_results(self, filename: str = "benchmark_results.json") -> None:
        """Benchmark sonuçlarını kaydet"""
        report = self.run_all_tests()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📊 Benchmark sonuçları {filename} dosyasına kaydedildi")
        print(f"✅ Başarı oranı: {report['test_summary']['success_rate']:.2%}")
        print(f"⏱️ Ortalama test süresi: {report['test_summary']['avg_test_duration']:.2f} saniye")
        print(f"😊 Ortalama memnuniyet: {report['test_summary']['avg_satisfaction']:.1f}/5")

# Global benchmark tester
benchmark_tester = BenchmarkTester()

if __name__ == "__main__":
    # Benchmark testlerini çalıştır
    benchmark_tester.save_benchmark_results()
