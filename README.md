# ESP32 Tabanlı Ses Kontrollü Multi-LED Sistemi

## Proje Hakkında
Bu proje, ESP32 mikrodenetleyicisini kullanarak ses komutları ile kontrol edilen bir LED sistemi tasarlamayı amaçlamaktadır. Bilgisayarın mikrofonu aracılığıyla ses verisi toplanır, makine öğrenme modeli ile işlenir ve bu model aracılığıyla LED'ler kontrol edilir. Proje, mikrodenetleyici programlamayı ve makine öğrenmesini birleştiren yenilikçi bir çözüm sunmaktadır.

## Amaç ve Özellikler
Bu projenin temel amacı, ses komutları ile LED kontrolünü sağlamak ve ses tanıma modelinin ESP32 ile entegre bir şekilde çalışmasını sağlamaktır. Projenin temel özellikleri şunlardır:
- **Ses Verisi Toplama ve İşleme:** Kullanıcılardan farklı çevresel koşullarda ses kayıtları toplanır ve eğitim için veri seti oluşturulur.
- **Makine Öğrenme Modeli Geliştirme:** Destek Vektör Makineleri (SVM) kullanılarak ses komutlarını tanıyabilen bir model geliştirilir.
- **ESP32 Entegrasyonu:** Modelin tahminleri, ESP32'nin GPIO pinleri üzerinden LED'leri kontrol etmek için kullanılır.
- **Esneklik:** Yeni komutlar ve LED'ler eklenerek sistemin genişletilebilirliği sağlanır.

## Kullanılan Bileşenler
### Donanım
- **ESP32 Mikrodenetleyici**  
- **LED'ler** (Kırmızı, Yeşil, Mavi)  
- **220Ω Dirençler** (LED'leri korumak için kullanılır)  
- **Bilgisayar Mikrofonu** (Ses kaydı için)  
- **Bağlantı Kabloları**  

### Yazılım Araçları
- **Python Kütüphaneleri:** 
  - NumPy, Pandas: Veri manipülasyonu için kullanılır.
  - Librosa: Ses işleme ve özellik çıkarımı için kullanılır.
  - Sounddevice: Mikrofon aracılığıyla ses kaydı almak için kullanılır.
  - Requests: HTTP istekleri göndermek için kullanılır.
  - Joblib: Eğitimli modeli kaydetmek ve yüklemek için kullanılır.
  - Scikit-learn: Makine öğrenme modelleri için kullanılır (Özellikle SVM).
  - Matplotlib ve Seaborn: Görselleştirme ve analiz için kullanılır.
  - PyDub ve Soundfile: Ses dosyalarını işlemek için kullanılır.
- **ESP32 Kütüphaneleri:** 
  - WiFi.h: ESP32'nin Wi-Fi bağlantısını sağlamak için kullanılır.
  - ArduinoJson.h: JSON formatındaki verileri işlemek için kullanılır.
  - WebServer.h: ESP32'yi bir web sunucusu olarak çalıştırmak için kullanılır.

## Veri Toplama ve İşleme
- **ZIP Dosyası Çıkarma:** Ses verileri sıkıştırılmış bir ZIP dosyasından çıkarılır.
- **Veri Seti:** Çeşitli ortam koşullarında kaydedilen ses verileri kullanıldı.
- **Format Dönüştürme:** m4a -> wav formatına dönüştürüldü.
- **Özellik Çıkarma:**
  - MFCC (Mel Frekans Kepstral Katsayıları)
  - Delta MFCC ve Spektral Kontrast
- **Veri Dengelenmesi:** SMOTE (Synthetic Minority Over-sampling Technique) uygulanarak eğitim verileri dengelendi.

## Model Eğitimi
- **Destek Vektör Makineleri (SVM) modeli kullanıldı.**
- **Veri Seçimi:** Önemli özellikler `SelectKBest` ile belirlendi.
- **Model Kaydetme:** Model, scaler ve seçici nesneleri `joblib` ile kaydedildi.
- **Model Tahmini:** Yeni ses verileri için tahmin yapılabiliyor.

## ESP32 Entegrasyonu
- **ESP32 Web Sunucusu ile HTTP POST Talepleri Alınıyor.**
- **ESP32 Kod Yapısı:**
  - JSON formatında gelen komutları işler.
  - LED’leri açıp kapatır.
  - Komutları Wi-Fi üzerinden alır.
- **Python tarafında HTTP POST istekleri gönderilerek komutlar ESP32'ye iletiliyor.**

## Karşılaşılan Sorunlar ve Çözümler
### Sorunlar
- **Gerçek zamanlı ses kayıtlarında tanıma güçlükleri:** İlk eğitim verisi yetersizdi ve yeni ses kayıtları eklendi.
- **Gürültülü ortamların model performansını düşürmesi:** Gürültü eklenmiş veri ile model eğitildi.
- **ESP32’ye komut gönderme gecikmeleri:** Web sunucu optimizasyonları yapıldı.

### Çözümler
- **Daha fazla ses verisi ile model eğitildi.**
- **Veri artırma (Data Augmentation) teknikleri kullanıldı.**
- **Wi-Fi bağlantı istikrarı artırıldı.**

## Sonuç
Bu proje ile sesle kontrol edilen bir LED sistemi başarıyla geliştirildi. Sistem, belirlenen beş farklı ses komutunu tanıyabilmekte ve %95 doğruluk oranıyla LED’leri kontrol edebilmektedir. Makine öğrenmesi ve mikrodenetleyici programlamasının birleşimiyle yenilikçi bir çözüm oluşturulmuştur. Gelecekte sistem, daha fazla komut ve donanım bileşeni ile genişletilebilir.

