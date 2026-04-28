# Akıllı Otopark Simülasyon Sistemi

## Proje Açıklaması

Bu proje, akıllı otopark yönetim sistemi için bir simülasyon uygulamasıdır. Python, SimPy ve Streamlit kullanılarak geliştirilmiştir. Sistem, park yeri arama süresini azaltarak yakıt tasarrufu sağlamayı hedefler.

## Özellikler

- **Simülasyon Motoru**: SimPy ile ayrık olay simülasyonu
- **Etkileşimli Arayüz**: Streamlit ile gerçek zamanlı görselleştirme
- **Dinamik Izgara**: Park yerlerinin doluluk durumuna göre renk değişimi
- **Gerçek Zamanlı Grafikler**: Doluluk oranı takibi
- **Detaylı Kayıtlar**: Araç giriş/çıkış logları

## Kurulum

1. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Uygulamayı çalıştırın:
   ```bash
   streamlit run src/app.py
   ```

## Kullanım

- Zaman kaydırıcısını kullanarak simülasyonu farklı zaman noktalarında inceleyin
- Park yeri haritasında yeşil (boş) ve kırmızı (dolu) renkleri gözlemleyin
- Doluluk oranı grafiğini takip edin
- İşlem kayıtlarında araç hareketlerini görün

## Teknik Detaylar

### Simülasyon Parametreleri
- Araç geliş aralığı: Üstel dağılım (ortalama 5 dakika)
- Park süresi: 15-45 dakika arası rastgele
- Toplam simülasyon süresi: 100 dakika
- Park yeri kapasitesi: 10

### Veri Yapısı
- Park yerleri JSON formatında koordinatlarla tanımlanır
- Simülasyon verileri log, doluluk geçmişi ve olay listesi olarak toplanır

## Sonuçlar

Bu sistem, akıllı otopark sistemlerinin etkinliğini simüle ederek, geleneksel park arama yöntemlerine kıyasla zaman ve yakıt tasarrufunu gösterir. Kullanıcı dostu arayüz sayesinde karar vericiler sisteme kolayca adapte olabilir.
