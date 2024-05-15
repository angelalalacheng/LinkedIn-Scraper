# LinkedIn-Scraper

## How to set up

1. Clone the project

```
git clone git@github.com:angelalalacheng/LinkedIn-Scraper.git

cd /path/to/project
```

2. Run the frontend

```
cd scraper
npm start
```

3. Run the Flask API(new another terminal)

```
cd API
pip3 install -r requirements.txt
python3 app.py
```

## How to use

1. Input your LinkedIn email and password
2. Input the LinkedIn post url then submit
3. If success, it will show the table about required details (name, LinkedIn URL, position, comment) for each commenter and you can download csv file as well by clicking the button

## How it works

![]("https://github.com/angelalalacheng/LinkedIn-Scraper/blob/main/flow.png")

## Challenge

1. Deploy the API as Web Service with some difficulties.
2. I tried deploying it using Docker on Render, Replit, and EC2, but none of these attempts were successful.
3. Many questions about installing Chrome and Driver on server.
