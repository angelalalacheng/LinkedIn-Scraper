import requests
import json
import re
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, email, password):
    driver.get("https://www.linkedin.com")
    sleep(10)
    user = driver.find_element(By.ID, "session_key")
    user.send_keys(email)
    sleep(0.5)
    pw = driver.find_element(By.ID,'session_password')
    pw.send_keys(password)
    sleep(0.5)
    sign_in_button = driver.find_element(By.XPATH,'//* [@type="submit"]')
    sign_in_button.click()
    
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "error-for-password"))
        )
        # print("Login Failed! Cannot continue scraping.")
        driver.quit()
        return False
    except Exception:
        print("Login Successful!")
    
    return True

def is_url_accessible(url):    
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        return False
    return True

def is_url_valid(url):
    if not re.match(r"https://www.linkedin.com/posts/.+", url):
        return False
    return True
    
def get_post_comments(driver, url):
    if not is_url_accessible(url):
        return {}, False

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)
        while True:
            load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "comments-comments-list__load-more-comments-button")))
            load_more_button.click()
            sleep(1)
    except Exception:
        print("# All comments have been loaded")
    finally:
        data = []
        comments = driver.find_elements(By.CLASS_NAME, "comments-comments-list__comment-item")
        for comment in comments:
            info = {}
            commenter = comment.find_element(By.CLASS_NAME, "comments-post-meta__profile-info-wrapper")
            commenterName = commenter.find_element(By.CLASS_NAME, "comments-post-meta__name-text").find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
            commenterLink = commenter.find_element(By.TAG_NAME, "a").get_attribute("href")
            commenterHeadline = commenter.find_element(By.CLASS_NAME, "comments-post-meta__headline").text
            commentContent = comment.find_element(By.CLASS_NAME, "comments-comment-item__main-content").text
            info['Name'] = commenterName
            info['Profile Link'] = commenterLink
            info['Current Position'] = extract_position(commenterHeadline)
            info['Comment'] = commentContent
            data.append(info)
        json_data = json.dumps(data)
        return json_data, True

def extract_position(commenterHeadline):
    if commenterHeadline=="":
        return "Not Available"
    
    if commenterHeadline.find("|") == -1:
        return commenterHeadline
    else:
        return commenterHeadline[:commenterHeadline.find("|")].strip()

# download or update ChromeDriver
# opts = Options()
# opts.add_argument("--headless")
# opts.add_argument("--disable-gpu")
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(options=opts, service=service)

# is_url_valid(url)
# login(driver, email, password)
# get_post_comments(driver, url)

# close the browser
# driver.quit()