from flask import Flask, request, render_template
import requests
import os

api_key = os.getenv("API_KEY")

url = f"https://data.fixer.io/api/latest?access_key={api_key}"



app = Flask(__name__) 

@app.route("/", methods=["GET", "POST"]) 
def index():
    if request.method == "POST":
        amount = request.form.get("amount")
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")

        response = requests.get(url, params={"base": from_currency, "symbols": to_currency}) #base: dönüştürülecek para birimi, symbols: dönüştürülecek para birimleri
        app.logger.info(response)
        data = response.json() #response'un json formatında verisini alıyoruz
        converted_amount = data["rates"][to_currency] * float(amount) #dönüştürülen para birimi
        
        return render_template("index.html", converted_amount=converted_amount) #dönüştürülen para birimi
    
    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)
