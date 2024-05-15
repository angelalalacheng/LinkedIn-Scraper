FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    xvfb \
    chromium \
    chromium-driver \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    fonts-liberation \
    libappindicator3-1 \
    libdbusmenu-glib4 \
    libdbusmenu-gtk3-4 \
    libxss1 \
    lsb-release \
    xdg-utils \
    ca-certificates \
    curl

# # Define Chrome and Chromedriver versions
# ENV CHROME_VERSION=124.0.6367.207
# ENV CHROMEDRIVER_VERSION=124.0.6367.207

# # Install Chrome
# RUN wget https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chrome-linux64.zip \
#     && unzip chrome-linux64.zip \
#     && mv chrome-linux64 /usr/local/bin/chrome \
#     && rm chrome-linux64.zip

# # Install Chromedriver
# RUN wget https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/mac-arm64/chromedriver-mac-arm64.zip \
#     && unzip chromedriver-linux64.zip \
#     && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
#     && chmod +x /usr/bin/chromedriver \
#     && rm -rf chromedriver-linux64.zip

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

# 設定環境變量
ENV DISPLAY=:99

EXPOSE 8080

EXPOSE 9222

# 啟動 Xvfb
CMD ["sh", "-c", "rm -f /tmp/.X99-lock && Xvfb :99 -screen 0 1280x720x16 & export DISPLAY=:99 && sleep 5 && python3 app.py"]