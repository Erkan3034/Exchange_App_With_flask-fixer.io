from flask import Flask, request, render_template, jsonify
import requests
import os
import logging

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Terminal'e çıktı
        logging.FileHandler('app.log')  # Dosyaya kaydet
    ]
)

api_key = os.getenv("API_KEY")
if not api_key:
    print("⚠️  UYARI: API_KEY environment variable bulunamadı!")
    print("Lütfen .env dosyası oluşturun ve API_KEY=your_api_key_here ekleyin")

url = f"https://data.fixer.io/api/latest?access_key={api_key}"

app = Flask(__name__)

def get_exchange_rates():
    """EUR bazında tüm kurları al"""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None, f"API hatası: {response.status_code}"
        
        data = response.json()
        if not data.get("success", False):
            return None, f"API Error: {data.get('error', {}).get('info', 'Bilinmeyen hata')}"
        
        return data.get("rates", {}), None
    except Exception as e:
        return None, f"Bağlantı hatası: {str(e)}"

def convert_currency(amount, from_currency, to_currency):
    """Para birimi çevirisi yap"""
    rates, error = get_exchange_rates()
    if error:
        return None, error
    
    # EUR bazında kurlar
    eur_rates = rates
    
    # Eğer EUR'dan çeviriyorsak direkt kullan
    if from_currency == "EUR":
        if to_currency not in eur_rates:
            return None, f"Para birimi bulunamadı: {to_currency}"
        rate = eur_rates[to_currency]
        return amount * rate, rate
    
    # Eğer EUR'a çeviriyorsak tersini al
    if to_currency == "EUR":
        if from_currency not in eur_rates:
            return None, f"Para birimi bulunamadı: {from_currency}"
        rate = 1 / eur_rates[from_currency]
        return amount * rate, rate
    
    # Cross-rate hesaplama (USD -> TRY gibi)
    if from_currency not in eur_rates:
        return None, f"Para birimi bulunamadı: {from_currency}"
    if to_currency not in eur_rates:
        return None, f"Para birimi bulunamadı: {to_currency}"
    
    # Cross-rate = (EUR/TO_CURRENCY) / (EUR/FROM_CURRENCY)
    # = (1/TO_RATE) / (1/FROM_RATE) = FROM_RATE / TO_RATE
    from_rate = eur_rates[from_currency]
    to_rate = eur_rates[to_currency]
    cross_rate = to_rate / from_rate
    
    return amount * cross_rate, cross_rate

@app.route("/", methods=["GET", "POST"]) 
def index():
    if request.method == "POST":
        try:
            amount = request.form.get("amount")
            from_currency = request.form.get("fromCurrency")
            to_currency = request.form.get("toCurrency")
            
            print(f"🔍 DEBUG: Amount: {amount}, From: {from_currency}, To: {to_currency}")
            app.logger.info(f"Converting {amount} {from_currency} to {to_currency}")
            
            if not api_key:
                error_msg = "API anahtarı bulunamadı!"
                app.logger.error(error_msg)
                return render_template("index.html", error=error_msg)
            
            # Para birimi çevirisi
            converted_amount, rate = convert_currency(float(amount), from_currency, to_currency)
            
            if converted_amount is None:
                error_msg = rate  # rate burada hata mesajı
                app.logger.error(error_msg)
                return render_template("index.html", error=error_msg)
            
            app.logger.info(f"Conversion successful: {amount} {from_currency} = {converted_amount} {to_currency}")
            print(f"✅ Başarılı: {amount} {from_currency} = {converted_amount} {to_currency}")
            
            return render_template("index.html", 
                                 converted_amount=converted_amount,
                                 rate=rate,
                                 from_currency=from_currency,
                                 to_currency=to_currency,
                                 amount=amount)
            
        except Exception as e:
            error_msg = f"Bir hata oluştu: {str(e)}"
            app.logger.error(error_msg)
            print(f"❌ HATA: {error_msg}")
            return render_template("index.html", error=error_msg)
    
    return render_template("index.html")

@app.route("/api/convert", methods=["POST"])
def api_convert():
    """AJAX için API endpoint"""
    try:
        data = request.get_json()
        amount = data.get("amount")
        from_currency = data.get("fromCurrency")
        to_currency = data.get("toCurrency")
        
        app.logger.info(f"API Convert: {amount} {from_currency} to {to_currency}")
        
        if not api_key:
            return jsonify({"error": "API anahtarı bulunamadı!"}), 400
        
        converted_amount, rate = convert_currency(float(amount), from_currency, to_currency)
        
        if converted_amount is None:
            return jsonify({"error": rate}), 400
        
        return jsonify({
            "converted_amount": converted_amount,
            "rate": rate,
            "from_currency": from_currency,
            "to_currency": to_currency
        })
        
    except Exception as e:
        app.logger.error(f"API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Flask uygulaması başlatılıyor...")
    print("📝 Loglar terminalde ve app.log dosyasında görünecek")
    print("🌐 http://localhost:5000 adresinde çalışacak")
    
    # Railway için production ayarları
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
