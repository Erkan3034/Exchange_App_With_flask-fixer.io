# Döviz Çevirici (Currency Converter)

Flask tabanlı döviz çevirici uygulaması. Fixer.io API kullanarak gerçek zamanlı döviz kurları ile çeviri yapar.

### Uygulamadan Kareler
![Uygulama Ekran Görüntüsü](img/ss.png)


## Kurulum

1. **Gerekli paketleri yükleyin:**
   ```bash
   pip install flask requests
   ```

2. **API Key alın:**
   - [Fixer.io](https://fixer.io/) adresine gidin
   - Ücretsiz hesap oluşturun
   - API key'inizi alın

3. **Environment variable ayarlayın:**
   
   **Windows (PowerShell):**
   ```powershell
   $env:API_KEY="your_api_key_here"
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   set API_KEY=your_api_key_here
   ```
   
   **Linux/Mac:**
   ```bash
   export API_KEY="your_api_key_here"
   ```

4. **Uygulamayı çalıştırın:**
   ```bash
   python app.py
   ```

5. **Tarayıcıda açın:**
   ```
   http://localhost:5000
   ```

## Özellikler

- ✅ USD, EUR, TRY ve diğer para birimleri arası çeviri
- ✅ Gerçek zamanlı döviz kurları
- ✅ Responsive tasarım
- ✅ Hata yönetimi
- ✅ Logging sistemi

## API Sınırlamaları

Fixer.io ücretsiz planında:
- Sadece EUR bazında kurlar alınabilir
- Cross-rate hesaplamaları otomatik olarak yapılır
- Günlük API çağrı limiti vardır

## Sorun Giderme

### "API anahtarı bulunamadı!" hatası
- API_KEY environment variable'ının doğru ayarlandığından emin olun
- API key'in geçerli olduğunu kontrol edin

### "Para birimi bulunamadı" hatası
- Desteklenen para birimlerini kontrol edin
- API'nin çalışır durumda olduğunu kontrol edin

## Desteklenen Para Birimleri

- TRY (Türk Lirası)
- USD (Amerikan Doları)
- EUR (Euro)
- GBP (İngiliz Sterlini)
- JPY (Japon Yeni)
- CAD (Kanada Doları)
- AUD (Avustralya Doları)
- CHF (İsviçre Frangı)
- CNY (Çin Yuanı)
- RUB (Rus Rublesi) 
- Daha fazlası