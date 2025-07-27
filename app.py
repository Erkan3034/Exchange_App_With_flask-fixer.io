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

@app.route("/", methods=["GET", "POST"]) 
def index():
    if request.method == "POST":
        try:
            amount = request.form.get("amount")
            from_currency = request.form.get("fromCurrency")  # HTML'deki name attribute'u
            to_currency = request.form.get("toCurrency")      # HTML'deki name attribute'u
            
            print(f"🔍 DEBUG: Amount: {amount}, From: {from_currency}, To: {to_currency}")
            app.logger.info(f"Converting {amount} {from_currency} to {to_currency}")
            
            if not api_key:
                error_msg = "API anahtarı bulunamadı!"
                app.logger.error(error_msg)
                return render_template("index.html", error=error_msg)
            
            # API çağrısı
            response = requests.get(url, params={"base": from_currency, "symbols": to_currency})
            app.logger.info(f"API Response Status: {response.status_code}")
            app.logger.info(f"API Response: {response.text}")
            
            if response.status_code != 200:
                error_msg = f"API hatası: {response.status_code}"
                app.logger.error(error_msg)
                return render_template("index.html", error=error_msg)
            
            data = response.json()
            app.logger.info(f"API Data: {data}")
            
            if "error" in data:
                error_msg = f"API Error: {data['error']}"
                app.logger.error(error_msg)
                return render_template("index.html", error=error_msg)
            
            if to_currency not in data.get("rates", {}):
                error_msg = f"Para birimi bulunamadı: {to_currency}"
                app.logger.error(error_msg)
                return render_template("index.html", error=error_msg)
            
            rate = data["rates"][to_currency]
            converted_amount = rate * float(amount)
            
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
        
        response = requests.get(url, params={"base": from_currency, "symbols": to_currency})
        
        if response.status_code != 200:
            return jsonify({"error": f"API hatası: {response.status_code}"}), 400
        
        data = response.json()
        
        if "error" in data:
            return jsonify({"error": data["error"]}), 400
        
        rate = data["rates"][to_currency]
        converted_amount = rate * float(amount)
        
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
    app.run(debug=True, host='0.0.0.0', port=5000)
