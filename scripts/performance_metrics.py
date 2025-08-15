"""
Performans Ölçümleme Sistemi - Teknik Şartname Gereksinimleri
KPI (Key Performance Indicator) ve benchmark sistemi
"""

import json
import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict

@dataclass
class CallMetrics:
    """Görüşme metrikleri"""
    call_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    customer_satisfaction: int = 0  # 1-5 arası
    success_rate: float = 0.0  # 0-1 arası
    error_count: int = 0
    context_switches: int = 0
    tool_calls: int = 0
    stt_accuracy: float = 0.0
    tts_quality: float = 0.0
    scenario_completed: bool = False
    scenario_type: str = ""
    customer_id: str = ""

@dataclass
class SystemMetrics:
    """Sistem metrikleri"""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    avg_call_duration: float = 0.0
    avg_customer_satisfaction: float = 0.0
    avg_success_rate: float = 0.0
    total_errors: int = 0
    system_uptime: float = 0.0
    peak_concurrent_calls: int = 0
    current_concurrent_calls: int = 0

class PerformanceTracker:
    """Performans takip sistemi"""
    
    def __init__(self):
        self.calls: List[CallMetrics] = []
        self.system_start_time = datetime.now()
        self.current_calls: Dict[str, CallMetrics] = {}
        self.scenario_stats: Dict[str, Dict] = {}
        
    def start_call(self, call_id: str, customer_id: str = "", scenario_type: str = "") -> str:
        """Yeni görüşme başlat"""
        call_metrics = CallMetrics(
            call_id=call_id,
            start_time=datetime.now(),
            customer_id=customer_id,
            scenario_type=scenario_type
        )
        
        self.current_calls[call_id] = call_metrics
        self.calls.append(call_metrics)
        
        # Senaryo istatistiklerini güncelle
        if scenario_type not in self.scenario_stats:
            self.scenario_stats[scenario_type] = {
                "total_calls": 0,
                "successful_calls": 0,
                "avg_duration": 0.0,
                "avg_satisfaction": 0.0
            }
        
        self.scenario_stats[scenario_type]["total_calls"] += 1
        
        return call_id
    
    def end_call(self, call_id: str, success: bool = True, satisfaction: int = 5) -> bool:
        """Görüşme sonlandır"""
        if call_id not in self.current_calls:
            return False
        
        call_metrics = self.current_calls[call_id]
        call_metrics.end_time = datetime.now()
        call_metrics.duration_seconds = (call_metrics.end_time - call_metrics.start_time).total_seconds()
        call_metrics.success_rate = 1.0 if success else 0.0
        call_metrics.customer_satisfaction = satisfaction
        call_metrics.scenario_completed = success
        
        # Senaryo istatistiklerini güncelle
        scenario_type = call_metrics.scenario_type
        if scenario_type in self.scenario_stats:
            if success:
                self.scenario_stats[scenario_type]["successful_calls"] += 1
        
        del self.current_calls[call_id]
        return True
    
    def log_error(self, call_id: str, error_type: str = "general") -> None:
        """Hata logla"""
        if call_id in self.current_calls:
            self.current_calls[call_id].error_count += 1
    
    def log_tool_call(self, call_id: str) -> None:
        """Araç çağrısı logla"""
        if call_id in self.current_calls:
            self.current_calls[call_id].tool_calls += 1
    
    def log_context_switch(self, call_id: str) -> None:
        """Bağlam değişimi logla"""
        if call_id in self.current_calls:
            self.current_calls[call_id].context_switches += 1
    
    def update_stt_accuracy(self, call_id: str, accuracy: float) -> None:
        """STT doğruluğunu güncelle"""
        if call_id in self.current_calls:
            self.current_calls[call_id].stt_accuracy = accuracy
    
    def update_tts_quality(self, call_id: str, quality: float) -> None:
        """TTS kalitesini güncelle"""
        if call_id in self.current_calls:
            self.current_calls[call_id].tts_quality = quality
    
    def get_system_metrics(self) -> SystemMetrics:
        """Sistem metriklerini hesapla"""
        completed_calls = [call for call in self.calls if call.end_time is not None]
        
        if not completed_calls:
            return SystemMetrics()
        
        total_calls = len(completed_calls)
        successful_calls = len([call for call in completed_calls if call.success_rate > 0.5])
        failed_calls = total_calls - successful_calls
        
        avg_duration = statistics.mean([call.duration_seconds for call in completed_calls])
        avg_satisfaction = statistics.mean([call.customer_satisfaction for call in completed_calls])
        avg_success_rate = statistics.mean([call.success_rate for call in completed_calls])
        
        total_errors = sum([call.error_count for call in completed_calls])
        system_uptime = (datetime.now() - self.system_start_time).total_seconds()
        
        return SystemMetrics(
            total_calls=total_calls,
            successful_calls=successful_calls,
            failed_calls=failed_calls,
            avg_call_duration=avg_duration,
            avg_customer_satisfaction=avg_satisfaction,
            avg_success_rate=avg_success_rate,
            total_errors=total_errors,
            system_uptime=system_uptime,
            current_concurrent_calls=len(self.current_calls)
        )
    
    def get_scenario_metrics(self) -> Dict[str, Dict]:
        """Senaryo bazlı metrikler"""
        scenario_metrics = {}
        
        for scenario_type, stats in self.scenario_stats.items():
            scenario_calls = [call for call in self.calls if call.scenario_type == scenario_type and call.end_time]
            
            if scenario_calls:
                avg_duration = statistics.mean([call.duration_seconds for call in scenario_calls])
                avg_satisfaction = statistics.mean([call.customer_satisfaction for call in scenario_calls])
                success_rate = len([call for call in scenario_calls if call.success_rate > 0.5]) / len(scenario_calls)
                
                scenario_metrics[scenario_type] = {
                    "total_calls": len(scenario_calls),
                    "successful_calls": len([call for call in scenario_calls if call.success_rate > 0.5]),
                    "success_rate": success_rate,
                    "avg_duration": avg_duration,
                    "avg_satisfaction": avg_satisfaction,
                    "avg_tool_calls": statistics.mean([call.tool_calls for call in scenario_calls]),
                    "avg_errors": statistics.mean([call.error_count for call in scenario_calls])
                }
        
        return scenario_metrics
    
    def generate_benchmark_report(self, test_scenarios: List[Dict]) -> Dict:
        """Benchmark raporu oluştur"""
        system_metrics = self.get_system_metrics()
        scenario_metrics = self.get_scenario_metrics()
        
        # 100 örnek test gereksinimi kontrolü
        total_test_calls = len([call for call in self.calls if call.scenario_type.startswith("test_")])
        
        report = {
            "report_generated": datetime.now().isoformat(),
            "test_summary": {
                "total_test_calls": total_test_calls,
                "minimum_required": 100,
                "requirement_met": total_test_calls >= 100
            },
            "system_performance": asdict(system_metrics),
            "scenario_performance": scenario_metrics,
            "kpi_analysis": {
                "success_rate": system_metrics.avg_success_rate,
                "customer_satisfaction": system_metrics.avg_customer_satisfaction,
                "avg_call_duration": system_metrics.avg_call_duration,
                "error_rate": system_metrics.total_errors / max(system_metrics.total_calls, 1),
                "system_reliability": (system_metrics.successful_calls / max(system_metrics.total_calls, 1)) * 100
            },
            "scaling_analysis": {
                "current_capacity": system_metrics.current_concurrent_calls,
                "peak_capacity": system_metrics.peak_concurrent_calls,
                "estimated_100k_calls_daily": {
                    "required_servers": max(1, int(100000 / (system_metrics.avg_call_duration * 3600))),
                    "estimated_cost_per_day": "Hesaplanacak",
                    "estimated_response_time": system_metrics.avg_call_duration
                }
            }
        }
        
        return report
    
    def save_metrics(self, filename: str = "performance_metrics.json") -> None:
        """Metrikleri dosyaya kaydet"""
        report = self.generate_benchmark_report([])
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    def load_metrics(self, filename: str = "performance_metrics.json") -> Dict:
        """Metrikleri dosyadan yükle"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

# Global performans takipçisi
performance_tracker = PerformanceTracker()

# KPI hesaplama fonksiyonları
def calculate_success_rate(calls: List[CallMetrics]) -> float:
    """Başarı oranını hesapla"""
    if not calls:
        return 0.0
    successful = len([call for call in calls if call.success_rate > 0.5])
    return successful / len(calls)

def calculate_customer_satisfaction(calls: List[CallMetrics]) -> float:
    """Müşteri memnuniyetini hesapla"""
    if not calls:
        return 0.0
    return statistics.mean([call.customer_satisfaction for call in calls])

def calculate_avg_call_duration(calls: List[CallMetrics]) -> float:
    """Ortalama görüşme süresini hesapla"""
    if not calls:
        return 0.0
    return statistics.mean([call.duration_seconds for call in calls])

def calculate_error_rate(calls: List[CallMetrics]) -> float:
    """Hata oranını hesapla"""
    if not calls:
        return 0.0
    total_errors = sum([call.error_count for call in calls])
    return total_errors / len(calls)
