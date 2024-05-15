FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# # Define Chrome and Chromedriver versions
ENV CHROME_VERSION=124.0.6367.207
ENV CHROMEDRIVER_VERSION=124.0.6367.207

# Install Chrome
RUN wget https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chrome-linux64.zip \
    && unzip chrome-linux64.zip \
    && mv chrome-linux64 /usr/local/bin/chrome \
    && rm chrome-linux64.zip

# Install Chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/mac-arm64/chromedriver-mac-arm64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

# # 設定環境變量
# ENV DISPLAY=:99

EXPOSE 8080

CMD ["python3", "app.py"]