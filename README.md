# Akıllı Ev Kontrol Sistemi

Bu proje, yapay zeka tabanlı bir akıllı ev otomasyon sistemidir. Sensör verilerini analiz ederek ev ortamını optimize eden ve kullanıcı davranışlarından öğrenen bir sistem sunar.

## 🏗️ Mimari Yapı

Sistem üç ana bileşenden oluşur:

1. **Sensör Katmanı** (`src/sensors.py`)
   - Sıcaklık sensörü (°C)
   - Nem sensörü (%)
   - Kapı durumu sensörü (açık/kapalı)
   - Hava kalitesi sensörü (PPM)
   - Varlık sensörü (var/yok)

2. **AI Kontrol Katmanı** (`src/ai_controller.py`, `src/ai_model.py`)
   - Karar ağacı tabanlı öğrenme sistemi
   - Sensör verisi analizi
   - Kural çıkarımı ve optimizasyon
   - Kullanıcı davranış analizi

3. **Frontend Arayüzü** (`frontend/index.html`)
   - Gerçek zamanlı sensör göstergeleri
   - Sistem durumu görüntüleme
   - Aktif kurallar tablosu
   - Aksiyon geçmişi

## 🤖 Yapay Zeka Sistemi

### Kullanılan AI Teknolojileri
- Karar Ağacı Sınıflandırıcısı (Decision Tree Classifier)
- Çoklu Çıktı Sınıflandırma (Multi-output Classification)
- Kural Çıkarım Sistemi (Rule Extraction System)

### Öğrenme Mekanizması
1. **Veri Toplama**
   - Sensör verilerinin periyodik kaydı
   - Kullanıcı tercihlerinin analizi
   - Ortam koşullarının izlenmesi

2. **Model Eğitimi**
   - Geçmiş verilerden örüntü çıkarımı
   - Optimum koşulların belirlenmesi
   - Kural setlerinin oluşturulması

3. **Akıllı Karar Verme**
   - Çoklu sensör verisi analizi
   - Kullanıcı davranış tahminlemesi
   - Otonom sistem kontrolü

## 📊 Veri Akışı

1. **Veri Toplama**
   ```
   Sensörler -> JSON Formatında Veri -> Veri İşleme
   ```

2. **İşleme ve Analiz**
   ```
   Ham Veri -> AI Model -> Karar Mekanizması
   ```

3. **Aksiyon Alma**
   ```
   Karar -> Sistem Kontrolü -> Durum Güncellemesi
   ```

## 🧪 Test Senaryoları

### Temel Testler (`tests/test_smart_home.py`)
1. Sensör veri doğrulama
2. AI model tepki testleri
3. Sistem entegrasyon testleri

### AI Model Testleri (`tests/test_ai_model.py`)
1. Öğrenme performansı
2. Kural çıkarım doğruluğu
3. Karar verme tutarlılığı

## 📝 Kullanım Örnekleri

### 1. Sıcaklık ve Nem Kontrolü
```python
# Örnek senaryo
Eğer sıcaklık > 25°C ve nem > 60%:
    - Havalandırma sistemi aktif
    - Nem alma modu başlat
```

### 2. Hava Kalitesi Yönetimi
```python
# Örnek senaryo
Eğer hava kalitesi > 1000 PPM ve varlık = True:
    - Pencere otomasyonu aktif
    - Havalandırma maksimum güç
```

### 3. Enerji Tasarrufu
```python
# Örnek senaryo
Eğer varlık = False ve sıcaklık normal aralıkta:
    - Sistemleri bekleme moduna al
    - Enerji tasarruf modu aktif
```

## 🛠️ Kurulum ve Çalıştırma

1. Gereksinimlerin Kurulumu
```bash
pip install -r requirements.txt
```

2. Sistemin Başlatılması
```bash
python simulate_smart_home.py
```

3. Web Arayüzüne Erişim
```
http://localhost:8000
```

## 📈 Performans Metrikleri

- Öğrenme doğruluğu: ~85%
- Tepki süresi: <100ms
- Sensör veri güncelleme sıklığı: 1sn

## 🔄 Sistem Kuralları

### Temel Kurallar
1. Konfor optimizasyonu
2. Enerji verimliliği
3. Hava kalitesi kontrolü

### Dinamik Kurallar
- Kullanıcı davranışlarına göre otomatik kural oluşturma
- Mevsimsel adaptasyon
- Zaman bazlı optimizasyon

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Branch'inizi push edin
5. Pull request oluşturun

## 📄 Lisans

MIT License
