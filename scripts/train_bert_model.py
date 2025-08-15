import json
import torch
import os
from pathlib import Path
from transformers import BertTokenizer, BertForSequenceClassification
from torch.optim import AdamW
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.model_selection import train_test_split

# Config dosyasını import et
try:
    from config import *
except ImportError:
    # Eğer config dosyası bulunamazsa, basit path hesaplama yap
    def get_project_root():
        current_file = Path(__file__).resolve()
        if current_file.parent.name == 'scripts':
            return current_file.parent.parent
        return current_file.parent
    PROJECT_ROOT = get_project_root()

class CagriMerkeziDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=64):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label)
        }

def load_train_data():
    # Örnek eğitim verileri
    train_data = [
        # Sim Kart İşlemleri (6, özel işlem)
        ("Sim kart şifremi unuttum", 6),
        ("Sim kartımın şifresini öğrenmek istiyorum", 6),
        ("Sim şifresini hatırlamıyorum", 6),
        ("Sim kart pin kodumu kaybettim", 6),
        ("Sim kartımın pin kodunu unuttum", 6),
        ("PUK kodumu öğrenmek istiyorum", 6),
        ("Sim kart şifresi alma", 6),
        ("Yeni sim kart şifresi istiyorum", 6),
        ("Sim kart şifre işlemleri", 6),
        ("Pin kodu alma", 6),
        
        # Fatura İtiraz (0)
        ("Faturamda anormal bir artış var, itiraz etmek istiyorum", 0),
        ("Son faturamda haksız kesinti var", 0),
        ("Bu ay faturama yansıyan ekstra ücretlere itiraz ediyorum", 0),
        ("Faturama itiraz etmek istiyorum", 0),
        ("Faturamda bir yanlışlık olduğunu düşünüyorum", 0),
        ("Geçen aya göre faturam çok yüksek gelmiş", 0),
        ("Bu ay faturama yansıyan ek ücretler var", 0),
        ("Faturamda anlamadığım ekstra ödemeler var", 0),
        ("Yurt dışı kullanım ücreti yanlış hesaplanmış", 0),
        ("Paket aşım ücretlerine itirazım var", 0),
        ("Faturamda tanımadığım hizmet ücretleri var", 0),
        ("Kullanmadığım hizmetler faturalandırılmış", 0),
        ("Faturamda bir hesaplama hatası var", 0),
        ("Ek paket ücretleri yanlış yansıtılmış", 0),
        ("Taahhüt indirimi yansımamış", 0),
        
        # Paket/Tarife Değişikliği (1)
        ("Tarifemi değiştirmek istiyorum", 1),
        ("Daha uygun bir pakete geçmek istiyorum", 1),
        ("Yeni tarife önerileriniz neler?", 1),
        ("Paketimi yükseltmek istiyorum", 1),
        ("Mevcut tarifemi güncellemek istiyorum", 1),
        ("Daha büyük bir internet paketi almak istiyorum", 1),
        ("Tarifemi küçültmek istiyorum", 1),
        ("Uygun fiyatlı bir tarife arıyorum", 1),
        ("Faturalıdan faturasıza geçmek istiyorum", 1),
        ("Kontörlü hattan faturalıya geçiş yapmak istiyorum", 1),
        ("Şu anki paketim yetersiz geliyor", 1),
        ("Tarifemi ailem için yükseltmek istiyorum", 1),
        ("İnternet paketimi artırmak istiyorum", 1),
        ("Dakika paketimi düşürmek istiyorum", 1),
        ("Yeni kampanyalı tarifeleri öğrenmek istiyorum", 1),
        
        # Borç/Ödeme Sorgusu (2)
        ("Kalan borcumu öğrenebilir miyim?", 2),
        ("Ne kadar borcum var?", 2),
        ("Son ödeme tarihim ne zaman?", 2),
        ("Fatura tutarımı öğrenebilir miyim?", 2),
        ("Ödenmeyen faturalarım var mı?", 2),
        ("Geçmiş dönem faturalarımı görebilir miyim?", 2),
        ("Faturamı online nasıl ödeyebilirim?", 2),
        ("Otomatik ödeme talimatı vermek istiyorum", 2),
        ("Geçen ayın fatura tutarını öğrenebilir miyim?", 2),
        ("Son ödediğim fatura ne kadardı?", 2),
        ("Bu ay faturama ne kadar yansıyacak?", 2),
        ("Kredi kartıyla ödeme yapmak istiyorum", 2),
        ("Taksitlendirme seçenekleri neler?", 2),
        ("Borç yapılandırması istiyorum", 2),
        ("Fatura detayımı görebilir miyim?", 2),
        
        # İptal Talebi (3)
        ("Hattımı kapatmak istiyorum", 3),
        ("İptal işlemi başlatmak istiyorum", 3),
        ("Aboneliğimi sonlandırmak istiyorum", 3),
        ("Hattımı iptal etmek istiyorum", 3),
        ("Hattımı kapatın lütfen", 3),
        ("İnternet aboneliğimi iptal etmek istiyorum", 3),
        ("Numara taşıma ile hattımı kapatacağım", 3),
        ("Yurt dışına taşınıyorum, hattımı kapatmam gerek", 3),
        ("Kontratımı feshetmek istiyorum", 3),
        ("Abonelik iptali için ne yapmam gerekiyor?", 3),
        ("Paketimi iptal etmek istiyorum", 3),
        ("Dijital yayın aboneliğimi sonlandıracağım", 3),
        ("Ek paketimi iptal edin", 3),
        ("İnternet hizmetimi durdurmak istiyorum", 3),
        ("Kampanya iptal işlemi başlatmak istiyorum", 3),
        
        # Yeni Hizmet/Paket Talebi (4)
        ("Fiber internet bağlatmak istiyorum", 4),
        ("Yeni hat almak istiyorum", 4),
        ("Ek paket almak istiyorum", 4),
        ("İkinci bir hat açtırmak istiyorum", 4),
        ("Yeni bir internet paketi almak istiyorum", 4),
        ("Evde internet başvurusu yapmak istiyorum", 4),
        ("Yeni kampanyalardan yararlanmak istiyorum", 4),
        ("Mobil internet paketi almak istiyorum", 4),
        ("Telefon hattı başvurusu yapacağım", 4),
        ("4.5G hizmeti açtırmak istiyorum", 4),
        ("Dijital TV paketi almak istiyorum", 4),
        ("Akıllı cihaz kampanyasına katılmak istiyorum", 4),
        ("Yurt dışı paketi satın almak istiyorum", 4),
        ("Haftalık internet paketi alacağım", 4),
        ("Numara taşımayla yeni hat açtırmak istiyorum", 4),
        
        # Teknik Sorun/Arıza (5)
        ("İnternet bağlantım çok yavaş", 5),
        ("Telefonum çekmiyor", 5),
        ("Arama yapamıyorum", 5),
        ("İnternet kesildi", 5),
        ("Şebeke sorunu yaşıyorum", 5),
        ("4.5G internetim çalışmıyor", 5),
        ("Modemim arızalandı", 5),
        ("Fiber internet bağlantım kesiliyor", 5),
        ("Telefon hattımda ses gitmiyor", 5),
        ("SMS gönderemiyorum", 5),
        ("İnternet hızım çok düştü", 5),
        ("Mobil veri açılmıyor", 5),
        ("Şebeke çekmiyor", 5),
        ("Modem sinyal sorunu var", 5),
        ("Teknik destek istiyorum", 5)
    ]

    texts, labels = zip(*train_data)
    return list(texts), list(labels)

def train_model():
    # Model ve tokenizer'ı yükle
    tokenizer = BertTokenizer.from_pretrained('dbmdz/bert-base-turkish-cased')
    model = BertForSequenceClassification.from_pretrained(
        'dbmdz/bert-base-turkish-cased', 
        num_labels=7  # -1 için ekstra sınıf eklendi
    )

    # Eğitim verilerini yükle
    texts, labels = load_train_data()
    
    # Veriyi eğitim ve test olarak ayır
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    # Dataset ve DataLoader oluştur
    train_dataset = CagriMerkeziDataset(train_texts, train_labels, tokenizer)
    val_dataset = CagriMerkeziDataset(val_texts, val_labels, tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8)

    # Eğitim parametreleri
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    optimizer = AdamW(model.parameters(), lr=5e-5, eps=1e-8)
    num_epochs = 10

    # Eğitim döngüsü
    print("Eğitim başlıyor...")
    best_accuracy = 0.0

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        for batch in train_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)

            optimizer.zero_grad()
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        # Validasyon
        model.eval()
        val_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['label'].to(device)

                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                val_loss += outputs.loss.item()
                predictions = torch.argmax(outputs.logits, dim=1)
                correct += (predictions == labels).sum().item()
                total += labels.size(0)

        train_loss = train_loss / len(train_loader)
        val_loss = val_loss / len(val_loader)
        accuracy = correct / total * 100

        print(f'Epoch {epoch + 1}/{num_epochs}:')
        print(f'Train Loss: {train_loss:.4f}')
        print(f'Val Loss: {val_loss:.4f}')
        print(f'Accuracy: {accuracy:.2f}%')

        # En iyi modeli kaydet
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            print(f"En iyi model kaydediliyor (accuracy: {accuracy:.2f}%)")
            model.save_pretrained(str(BERTURK_CAGRI_MODEL_DIR))
            tokenizer.save_pretrained(str(BERTURK_CAGRI_MODEL_DIR))

    print("Eğitim tamamlandı!")

if __name__ == "__main__":
    train_model()
