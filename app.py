from flask import Flask, request, render_template
import requests
import os

api_key = os.getenv("API_KEY")

url = f"https://data.fixer.io/api/latest?access_key={api_key}"



app = Flask(__name__) 

@app.route("/")
def index():
    return render_template("index.html")





if __name__ == "__main__":
    app.run(debug=True)
