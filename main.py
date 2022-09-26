import io
import pickle
from multiprocessing import Pool
import requests
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from tqdm import tqdm
import os
import dill


def get_image_images(url):
    with open('archived_urls.pickle', 'rb') as f:
        finished_urls = dill.load(f)
        f.close()


    if url in finished_urls:
        return

    driver = webdriver.Chrome("D:\\chromedriver.exe")
    driver.get(url)
    driver.implicitly_wait(5)
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f'//*[@id="pagewrapper"]/div[1]/div[3]/div[3]/div[1]'))).click()

    name = driver.find_element(By.XPATH, f'//*[@id="newscol2"]/h1')
    name = name.text
    name = name.replace('/', '_')
    name = name.replace("'", '_')
    name = name.replace('"', '_')
    name = name.replace(':', ',')

    dir = os.path.join(r'D:\Data\Image_Without_Bounding_Box', name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        driver.quit()
        return

    for i in range(0, 1000):
        try:
            IMAGE_URL = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="swipebox-img-{i}"]'))).get_attribute('src')
            driver.find_element(By.XPATH, f'//*[@id="swnav_right"]').click()
            image_content = requests.get(IMAGE_URL).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            image.save(f'D:\\Data\\Image_Without_Bounding_Box\\{name}\\{i}.jpg')
        except:
            driver.quit()
            return




def get_page_urls():
    driver = webdriver.Chrome("D:\\chromedriver.exe")
    driver.get('https://www.autoevolution.com/carfinder/')
    driver.implicitly_wait(5)

    driver.find_element(By.XPATH, '//*[@id="cookienotif"]/a[1]').click()
    driver.find_element(By.XPATH, '//*[@id="carfform"]/div[1]/div[2]/div[3]/div[2]/div/div/span').click()
    driver.find_element(By.XPATH, '//*[@id="carfform"]/div[1]/div[2]/div[3]/div[2]/div/ul/li[2]').click()
    driver.find_element(By.XPATH, '//*[@id="carfstart"]/i').click()

    all_urls = []

    for i in tqdm(range(4, 6778)):
        make = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="pagewrapper"]/div[{i}]/div[2]/h5/a')))
        all_urls.append(make.get_attribute('href'))

    return all_urls


# run only first time you install program to create a pickle file

def first_time():
    all_urls = get_page_urls()
    with open('all_urls.dat', 'wb') as f:
        dill.dump(all_urls, f)


# second time onwards, you can just run the main() function. It will load the urls from the pickle file and run the get_image_images() function on all the urls.

def main():
    with open('all_urls.dat', 'rb') as f:
        all_urls = dill.load(f)

    all_urls = all_urls
    url_length = len(all_urls)

    with Pool(processes=10, maxtasksperchild=30) as p:
        r = list(tqdm(p.imap(get_image_images, all_urls), total=url_length))


if __name__ == '__main__':  # look at how far it goes in the function then slice said list at the point
    main()
