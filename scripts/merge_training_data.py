"""
Eğitim Verisi Birleştirme Scripti - TEKNOFEST 2025
3 eğitim dosyasını birleştirip tek dosya haline getirme
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import json

class TrainingDataMerger:
    """Eğitim verisi birleştirme sınıfı"""
    
    def __init__(self):
        self.target_categories = {
            "fatura itirazı": 1900,
            "paket kalan sorgulama": 1850,
            "borç sorgulama": 1800,
            "iptal talebi": 1750,
            "yeni paket/kampanya talebi": 1700,
            "teknik arıza": 850,
            "sim card/şifre işlemleri": 814
        }
        self.total_target = 10664
        
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """Veri dosyalarını yükle"""
        print("📂 Veri dosyaları yükleniyor...")
        
        df1 = pd.read_csv('data/egitim_veri1.csv')
        df2 = pd.read_csv('data/egitim_veri2.csv')
        df3 = pd.read_csv('data/egitim_veri3.csv')
        
        print(f"✅ Dosya 1 yüklendi: {len(df1)} satır")
        print(f"✅ Dosya 2 yüklendi: {len(df2)} satır")
        print(f"✅ Dosya 3 yüklendi: {len(df3)} satır")
        
        return {
            "df1": df1,
            "df2": df2,
            "df3": df3
        }
    
    def analyze_current_data(self, dataframes: Dict[str, pd.DataFrame]) -> Dict:
        """Mevcut veri analizi"""
        print("\n📊 Mevcut Veri Analizi:")
        print("=" * 50)
        
        df1, df2, df3 = dataframes["df1"], dataframes["df2"], dataframes["df3"]
        
        # Kategori sayılarını hesapla
        all_categories = {}
        
        for df_name, df in [("Dosya 1", df1), ("Dosya 2", df2), ("Dosya 3", df3)]:
            print(f"\n{df_name} kategorileri:")
            cat_counts = df['Category'].value_counts()
            for cat, count in cat_counts.items():
                if cat not in all_categories:
                    all_categories[cat] = 0
                all_categories[cat] += count
                print(f"  - {cat}: {count}")
        
        print(f"\n📈 Toplam kategori dağılımı:")
        for cat, count in all_categories.items():
            print(f"  - {cat}: {count}")
        
        total_rows = len(df1) + len(df2) + len(df3)
        print(f"\n📊 Toplam satır sayısı: {total_rows}")
        
        return {
            "current_categories": all_categories,
            "total_rows": total_rows,
            "dataframes": dataframes
        }
    
    def merge_data(self, dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Verileri birleştir"""
        print("\n🔄 Veriler birleştiriliyor...")
        
        df1, df2, df3 = dataframes["df1"], dataframes["df2"], dataframes["df3"]
        
        # Verileri birleştir
        merged_df = pd.concat([df1, df2, df3], ignore_index=True)
        
        print(f"✅ Birleştirme tamamlandı: {len(merged_df)} satır")
        
        return merged_df
    
    def clean_and_balance_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Veriyi temizle ve dengele"""
        print("\n🧹 Veri temizleme ve dengeleme...")
        
        # NaN değerleri temizle
        df = df.dropna()
        
        # Label sütununu oluştur (kategori ID'leri)
        category_to_id = {
            "fatura itirazı": 0,
            "paket kalan sorgulama": 1,
            "borç sorgulama": 2,
            "iptal talebi": 3,
            "yeni paket/kampanya talebi": 4,
            "teknik arıza": 5,
            "sim card/şifre işlemleri": 6
        }
        
        df['Label'] = df['Category'].map(category_to_id)
        
        # Kategori sayılarını kontrol et
        current_counts = df['Category'].value_counts()
        print("\n📊 Mevcut kategori dağılımı:")
        for cat, count in current_counts.items():
            target = self.target_categories.get(cat, 0)
            print(f"  - {cat}: {count} (hedef: {target})")
        
        # Veriyi hedef sayılara göre dengele
        balanced_dfs = []
        
        for category, target_count in self.target_categories.items():
            category_df = df[df['Category'] == category]
            current_count = len(category_df)
            
            if current_count >= target_count:
                # Fazla veriyi rastgele seç
                balanced_df = category_df.sample(n=target_count, random_state=42)
            else:
                # Eksik veriyi tekrarlayarak tamamla
                if current_count > 0:
                    # Mevcut veriyi tekrarla
                    repeat_times = target_count // current_count
                    remainder = target_count % current_count
                    
                    repeated_df = pd.concat([category_df] * repeat_times, ignore_index=True)
                    if remainder > 0:
                        additional_df = category_df.sample(n=remainder, random_state=42)
                        repeated_df = pd.concat([repeated_df, additional_df], ignore_index=True)
                    
                    balanced_df = repeated_df
                else:
                    # Bu kategori için veri yoksa boş DataFrame oluştur
                    balanced_df = pd.DataFrame(columns=df.columns)
            
            balanced_dfs.append(balanced_df)
            print(f"  ✅ {category}: {len(balanced_df)} satır")
        
        # Dengelenmiş verileri birleştir
        final_df = pd.concat(balanced_dfs, ignore_index=True)
        
        # Karıştır
        final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print(f"\n✅ Dengeleme tamamlandı: {len(final_df)} satır")
        
        return final_df
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Veriyi doğrula"""
        print("\n🔍 Veri doğrulama...")
        
        # Toplam satır sayısı kontrolü
        if len(df) != self.total_target:
            print(f"❌ Toplam satır sayısı hatalı: {len(df)} (hedef: {self.total_target})")
            return False
        
        # Kategori sayıları kontrolü
        category_counts = df['Category'].value_counts()
        for category, target_count in self.target_categories.items():
            actual_count = category_counts.get(category, 0)
            if actual_count != target_count:
                print(f"❌ {category} sayısı hatalı: {actual_count} (hedef: {target_count})")
                return False
        
        # Label değerleri kontrolü
        label_counts = df['Label'].value_counts().sort_index()
        expected_labels = list(range(7))
        for label in expected_labels:
            if label not in label_counts:
                print(f"❌ Label {label} eksik")
                return False
        
        print("✅ Veri doğrulama başarılı!")
        print(f"📊 Toplam satır: {len(df)}")
        print(f"🏷️ Kategori sayısı: {len(category_counts)}")
        print(f"📈 Label sayısı: {len(label_counts)}")
        
        return True
    
    def save_merged_data(self, df: pd.DataFrame, filename: str = "data/berturk_egitim_verisi_10664_7kategori.csv") -> None:
        """Birleştirilmiş veriyi kaydet"""
        print(f"\n💾 Veri kaydediliyor: {filename}")
        
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"✅ Veri başarıyla kaydedildi: {filename}")
        
        # Özet istatistikleri yazdır
        print("\n📊 Final Veri Özeti:")
        print("=" * 50)
        print(f"Toplam satır: {len(df)}")
        print(f"Kategori sayısı: {len(df['Category'].unique())}")
        print(f"Label sayısı: {len(df['Label'].unique())}")
        
        print("\nKategori dağılımı:")
        category_counts = df['Category'].value_counts()
        for category, count in category_counts.items():
            print(f"  - {category}: {count}")
        
        print("\nLabel dağılımı:")
        label_counts = df['Label'].value_counts().sort_index()
        for label, count in label_counts.items():
            category = df[df['Label'] == label]['Category'].iloc[0]
            print(f"  - Label {label} ({category}): {count}")
    
    def create_data_summary(self, df: pd.DataFrame) -> Dict:
        """Veri özeti oluştur"""
        summary = {
            "total_samples": len(df),
            "categories": len(df['Category'].unique()),
            "labels": len(df['Label'].unique()),
            "category_distribution": df['Category'].value_counts().to_dict(),
            "label_distribution": df['Label'].value_counts().sort_index().to_dict(),
            "columns": list(df.columns),
            "data_types": df.dtypes.to_dict()
        }
        
        # Özet dosyasını kaydet
        with open('data/berturk_egitim_verisi_ozeti.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        
        print("✅ Veri özeti kaydedildi: data/berturk_egitim_verisi_ozeti.json")
        
        return summary
    
    def run_merge_process(self) -> pd.DataFrame:
        """Tüm birleştirme sürecini çalıştır"""
        print("🚀 Eğitim Verisi Birleştirme Süreci Başlatılıyor")
        print("=" * 60)
        
        # 1. Verileri yükle
        dataframes = self.load_data()
        
        # 2. Mevcut veriyi analiz et
        analysis = self.analyze_current_data(dataframes)
        
        # 3. Verileri birleştir
        merged_df = self.merge_data(dataframes)
        
        # 4. Veriyi temizle ve dengele
        balanced_df = self.clean_and_balance_data(merged_df)
        
        # 5. Veriyi doğrula
        if not self.validate_data(balanced_df):
            print("❌ Veri doğrulama başarısız!")
            return None
        
        # 6. Birleştirilmiş veriyi kaydet
        self.save_merged_data(balanced_df)
        
        # 7. Veri özeti oluştur
        self.create_data_summary(balanced_df)
        
        print("\n🎉 Eğitim verisi birleştirme süreci tamamlandı!")
        return balanced_df

# Ana çalıştırma
if __name__ == "__main__":
    merger = TrainingDataMerger()
    final_data = merger.run_merge_process()
