import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import InvalidSchema
from binascii import a2b_base64
from binascii import Error
import urllib.request
import atexit
import requests
import shutil





def scroll_to_bottom(d):
    print("scrolling to bottom")
    d.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    sleep(0.5)

def show_more_results(d):
    print("showing more results")
    xpath = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[3]/div[2]/input"
    try:
        d.find_element_by_xpath(xpath).click()
        sleep(0.5)
        scroll_to_bottom(d)
    except Exception as e:
        print("show more results error")

def retry_button(d):
    print("retry button")
    xpath = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[3]/div[1]/div[2]/div[3]/div/span"
    try:
        d.find_element_by_xpath(xpath).click()
        sleep(0.5)
        scroll_to_bottom(d)
    except Exception as e:
        print("retry button error")

def end_reached(d):
    xpath = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[3]/div[1]/div[2]/div[1]/div"

    try:
        d.find_element_by_xpath(xpath).click()
        return True
    except Exception as e:
        print("end not reached")
        return False

def get_img_url(i, d):
    xpath = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/span/div[1]/div[1]/div[%s]/a[1]/div[1]/img" % str(i + 1)
    return d.find_element_by_xpath(xpath).get_attribute('src')

def download_imgs(urls):
    for i in range(len(urls)):
        print(urls[i])
        try:
            r = requests.get(urls[i])
            if "png" in urls[i]:
                with open("pictures/image%s.png" % i, "wb") as f:
                    f.write(r.content)
                    f.close()
            elif "jpeg" in urls[i]:
                with open("pictures/image%s.jpeg" % i, "wb") as f:
                    f.write(r.content)
                    f.close()
            elif "gif" in urls[i]:
                with open("pictures/image%s.gif" % i, "wb") as f:
                    f.write(r.content)
                    f.close()


        except InvalidSchema:
            data = urls[i]
            try:
                binary_data = a2b_base64(data)
                if "png" in urls[i]:
                    with open("pictures/image%s.png" % i, 'wb') as f:
                        f.write(binary_data)
                        f.close()
                elif "jpeg" in urls[i]:
                    with open("pictures/image%s.jpeg" % i, 'wb') as f:
                        f.write(binary_data)
                        f.close()
                elif "gif" in urls[i]:
                    with open("pictures/image%s.gif" % i, 'wb') as f:
                        f.write(binary_data)
                        f.close()
            except Error:
                pass




def run(SEARCH_TERM, token):
    os.mkdir(token)
    urls = []
    img_counter = 0
    BROWSER_OPTIONS = Options()
    BROWSER_OPTIONS.headless = True
    BROWSER_OPTIONS.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    BROWSER_OPTIONS.add_argument("--disable-dev-shm-usage")
    BROWSER_OPTIONS.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH") , options=BROWSER_OPTIONS)

    driver.get("http://www.google.com/images?q=" + SEARCH_TERM.replace(' ', '+'))

    while end_reached(driver) == False:
        scroll_to_bottom(driver)
        show_more_results(driver)
        retry_button(driver)
        end_reached(driver)

    for i in range(200):
        try:
            img_url = get_img_url(i, driver)
            if str(img_url) != "None":
                if "png" in img_url:
                    urllib.request.urlretrieve(img_url, "%s/img%s.png" % (token, img_counter))
                elif "jpeg" in img_url:
                    urllib.request.urlretrieve(img_url, "%s/img%s.jpeg" % (token, img_counter))
                elif "gif" in img_url:
                    urllib.request.urlretrieve(img_url, "%s/img%s.gif" % (token, img_counter))
                else:
                    urllib.request.urlretrieve(img_url, "%s/img%s.png" % (token, img_counter))

                img_counter += 1
            urls.append(img_url)

        except Exception as e:
            print(e)

    #download_imgs(urls,driver)
    shutil.make_archive(token, 'zip', token)
    driver.quit()

    return img_counter



'''
def main():
    try:
        
    finally:
        driver.close()
'''
if __name__=='__main__':
    run()
