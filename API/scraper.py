import requests
import json
import re
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, email, password):
    driver.get("https://www.linkedin.com")
    sleep(10) # wait for page to load because using headless mode
    user = driver.find_element(By.ID, "session_key")
    user.send_keys(email)
    sleep(0.5) # mimic human behavior
    pw = driver.find_element(By.ID,'session_password')
    pw.send_keys(password)
    sleep(0.5)
    sign_in_button = driver.find_element(By.XPATH,'//* [@type="submit"]')
    sign_in_button.click()
    
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "error-for-password"))
        )
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
    # check if URL is a LinkedIn post URL
    if not re.match(r"https://www.linkedin.com/posts/.+", url):
        return False
    return True

def get_post_comments(driver, url):
    if not is_url_accessible(url):
        return {}, False
    
    driver.get(url)
    # show all comments by clicking 'Load more' buttons
    click_load_more_buttons(driver)
    # show all replies by clicking 'Show previous replies' buttons
    click_show_prev_replies_buttons(driver)

    data = []
    comments = driver.find_elements(By.CLASS_NAME, "comments-comments-list__comment-item")
    for comment in comments:
        info = extract_comment_info(comment)
        data.append(info)

        replies_list = comment.find_elements(By.CLASS_NAME, "comments-comment-item__replies-list")
        for replies in replies_list:
            scrape_replies(driver, replies, data)

    return json.dumps(data), True

def extract_comment_info(comment):
    info = {}
    commenter = comment.find_element(By.CLASS_NAME, "comments-post-meta__profile-info-wrapper")
    commenterName = get_commenter_name(commenter)
    commenterLink = commenter.find_element(By.TAG_NAME, "a").get_attribute("href")
    commenterHeadline = commenter.find_element(By.CLASS_NAME, "comments-post-meta__headline").text
    commentContent = comment.find_element(By.CLASS_NAME, "comments-comment-item__main-content").text
    
    info['Name'] = commenterName
    info['Profile Link'] = commenterLink
    info['Current Position'] = extract_position(commenterHeadline)
    info['Comment'] = commentContent
    return info

def scrape_replies(driver, reply_element, data):
    replies = reply_element.find_elements(By.CLASS_NAME, "comments-reply-item")
    for reply_comment in replies:
        reply_info = extract_comment_info(reply_comment)
        data.append(reply_info)
        # recursively scrape replies to replies
        scrape_replies(driver, reply_comment, data)

def get_commenter_name(commenter):
    # I found that if the commenter is company account, it doesn't have span[aria-hidden='true']
    # otherwise, if the commenter is a person, it has span[aria-hidden='true']
    try:
        return commenter.find_element(By.CLASS_NAME, "comments-post-meta__name-text").find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text
    except:
        return commenter.find_element(By.CLASS_NAME, "comments-post-meta__name-text").text 

def extract_position(commenterHeadline):
    if not commenterHeadline:
        return "Not Available"
    return commenterHeadline.split("|")[0].strip() if "|" in commenterHeadline else commenterHeadline

def click_load_more_buttons(driver):
    while True:
        try:
            button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "comments-comments-list__load-more-comments-button"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            sleep(1)  # wait for more comments to load
        except:
            break

def click_show_prev_replies_buttons(driver):
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.show-prev-replies")
        for button in buttons:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                driver.execute_script("arguments[0].click();", button)
                sleep(0.5)
            except:
                print("Could not click 'show-prev-replies' button")
    except:
        print("No 'show-prev-replies' buttons found")