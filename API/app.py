import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def hello_world():
    return "Hello, LinkedIn Scraper!"

@app.route("/scrape", methods=['POST'])
def scrape():
    input = request.get_json()
    if not input:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    url = input['url']
    email = input['email']
    password = input['password']

    if not scraper.is_url_valid(url):
        return jsonify({'error': 'Invalid LinkedIn URL'}), 400

    opts = Options()
    service = Service(ChromeDriverManager().install())
    # service = Service('/usr/bin/chromedriver')
    opts.add_argument('--headless') 
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=opts, service=service)

    if not scraper.login(driver, email, password):
        return jsonify({'error': 'Invalid LinkedIn credentials. Cannot continue scraping.'}), 400
    
    data, success = scraper.get_post_comments(driver, url)

    if not success:
        return jsonify({'error': 'LinkedIn post URL is not accessible.'}), 400
    
    driver.quit()

    return data, 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
