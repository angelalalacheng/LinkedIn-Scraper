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

## Challenge

1. I'm facing difficulties with my LinkedIn crawler which can only operate in headful mode, making deployment more challenging because it requires a GUI.
2. I tried deploying it using Docker on Render, Replit, and EC2, but none of these attempts were successful.
