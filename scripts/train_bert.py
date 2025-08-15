import json
import torch
import os
from pathlib import Path
from transformers import BertTokenizer, BertForSequenceClassification
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

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

class MusteriDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=64):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def load_data(file_path):
    texts = []
    labels = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    texts.append(data['text'])
                    labels.append(data['label'])
                except json.JSONDecodeError as e:
                    print(f"JSON decode error on line: {line}")
                    print(f"Error: {str(e)}")
                    continue
                except KeyError as e:
                    print(f"Missing key in data: {str(e)}")
                    continue
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return [], []
    
    if not texts or not labels:
        print(f"No data loaded from {file_path}")
        return [], []
    
    print(f"Loaded {len(texts)} samples")
    return texts, labels

def train_model():
    # Veri setini yükle
    texts, labels = load_data(str(TRAIN_BERTURK_FILE))
    
    # Model ve tokenizer'ı yükle
    tokenizer = BertTokenizer.from_pretrained('dbmdz/bert-base-turkish-cased')
    model = BertForSequenceClassification.from_pretrained('dbmdz/bert-base-turkish-cased', num_labels=8)
    
    # Dataset ve DataLoader oluştur
    dataset = MusteriDataset(texts, labels, tokenizer)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
    
    # Optimizer
    optimizer = AdamW(model.parameters(), lr=5e-5)
    
    # Eğitim döngüsü
    num_epochs = 10
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.train()
    
    print(f"\nEğitim başlıyor... (Device: {device})")
    
    for epoch in range(num_epochs):
        total_loss = 0
        progress_bar = tqdm(dataloader, desc=f'Epoch {epoch + 1}/{num_epochs}')
        
        for batch in progress_bar:
            # Batch'i device'a taşı
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            # Forward pass
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()
            
            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Progress bar güncelle
            progress_bar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        avg_loss = total_loss / len(dataloader)
        print(f'\nEpoch {epoch + 1} - Ortalama kayıp: {avg_loss:.4f}')
    
    print("\nEğitim tamamlandı!")
    
    # Modeli kaydet
    print("\nModel kaydediliyor...")
    model_save_path = 'models/berturk_cagri_model'
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    print(f"Model kaydedildi: {model_save_path}")

if __name__ == "__main__":
    train_model()
