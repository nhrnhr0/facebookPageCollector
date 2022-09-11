from urllib.parse import urlsplit
from selenium.webdriver.common.by import By

DATA_DIR = "./data"


def get_search_keywords():
    # read file ../מילות חיפוש.txt line by line
    # return list of keywords
    with open(DATA_DIR + "/מילות חיפוש.txt", "r", encoding="utf-8") as f:
        keywords = f.readlines()
        keywords = [keyword.strip() for keyword in keywords]
    return keywords


# get .././מקומות לחיפוש.txt
# example:
# אופקים
# https://www.facebook.com/search/pages?q=test&filters=eyJmaWx0ZXJfcGFnZXNfbG9jYXRpb246MCI6IntcIm5hbWVcIjpcImZpbHRlcl9wYWdlc19sb2NhdGlvblwiLFwiYXJnc1wiOlwiMTE0NDg1MDM4NTY4MTg5XCJ9In0%3D
# נתיבות
# https://www.facebook.com/search/pages?q=test&filters=eyJmaWx0ZXJfcGFnZXNfbG9jYXRpb246MCI6IntcIm5hbWVcIjpcImZpbHRlcl9wYWdlc19sb2NhdGlvblwiLFwiYXJnc1wiOlwiMTA4MzM5OTE1ODU0NjM4XCJ9In0%3D
# extract the filters part of the query string
def get_locations():
    # read file ../מקומות לחיפוש.txt line by line
    # return list of locations
    with open(DATA_DIR + "/מקומות לחיפוש.txt", "r", encoding="utf-8") as f:
        locations = f.readlines()
        # split to location names and urls
        ret = []
        url = None
        location = None
        for line in locations:
            if line.strip().startswith("https"):
                url = line.strip()
                location = urlsplit(url).query.split("&")[1]
            else:
                if location:
                    ret.append({"name": name, "location": location})
                    location = None
                    url = None
                name = line.strip()
        if location:
            ret.append({"name": name, "location": location})
    return ret


def check_is_login(driver):
    try:
        el = driver.find_element(
            by=By.XPATH,
            value="//*[contains(text(), 'Join Facebook or log in to continue.')]",
        )
        return False
    except Exception as e:
        try:
            el = driver.find_element(
                By.XPATH, value="//*[contains(text(), 'Join or Log Into Facebook')]"
            )
            return False
        except Exception as e:
            try:
                # Log into Facebook
                el = driver.find_element(
                    By.XPATH, value="//*[contains(text(), 'Log into Facebook')]"
                )
                return False
            except Exception as e:
                print("yes login")
                return True
