import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


class TargetWebScrapping:
    """Class to get data from Target page"""
    def __init__(self):
        driver = None
        data = None

    def _get_answers(self, element):
        return [answer.text for answer in element.find_elements(By.XPATH, './/span[@data-test="answerText"]')]
    
    def define_driver(self):
        webdriver_service = Service(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')

        self.driver = webdriver.Chrome(options = options, service = webdriver_service)

    def get_data(self, url):
        self.driver.get(url)
        delay = 10
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//h1[@itemprop="name"]')))
            print('Page loaded successfully!')
        except TimeoutException:
            print('Page Load Time Exceeded!')
        
        self.driver.find_element(By.XPATH, '//body').send_keys(Keys.PAGE_UP)
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, -250);")

        self.driver.find_element(By.XPATH, '//button[@data-test="toggleContentButton"]').click()
        time.sleep(3)
        
        ##### Get Data #####    
        self.data = dict()
        self.data['title'] = self.driver.find_element(By.XPATH, '//h1[@data-test="product-title"]').text
        self.data['price'] = re.findall('\d*\.\d*', self.driver.find_element(By.XPATH, '//span[@data-test="da-price--monthly-price"]').text)[0]
        self.data['description'] = self.driver.find_element(By.XPATH, '//*[@id="specAndDescript"]/div[1]/div[2]/div[1]').text

        # Get Especifications
        conteiner = self.driver.find_element(By.XPATH, '//*[@id="specAndDescript"]/div[1]/div[1]').find_elements(By.TAG_NAME, 'div')
        specifications_dic = {}
        for div in conteiner:
            try:
                spec_title = div.find_element(By.XPATH, './/b[1]').text
                specifications_dic[spec_title] = div.text.replace(spec_title, '')
            except:
                continue
        self.data['specifications'] = specifications_dic
        
        # Get Highlights
        conteiner = self.driver.find_element(By.XPATH, '//*[@id="tabContent-tab-Details"]/div/div/div/div[1]/div[2]/div/ul/div').find_elements(By.TAG_NAME, 'span')
        highlights_list = [div.text for div in conteiner]
        self.data['highlights'] = highlights_list
        
        # Get Images Urls
        conteiner = self.driver.find_element(By.XPATH, './/div[@data-test="product-image"]').find_elements(By.TAG_NAME, 'img')
        images_list = []
        for img in conteiner:
            try:
                img_src = img.get_attribute("src")
                if 'data:image' not in img_src:
                    images_list.append(img_src)
            except:
                continue
        self.data['images_urls'] = images_list
        
        # Get Questions
        number_tabs = len(self.driver.find_element(By.XPATH, '//*[@id="product-details-tabs"]/div/div[1]/div[2]/ul').find_elements(By.TAG_NAME, 'li'))
        self.driver.find_element(By.XPATH, '//*[@id="product-details-tabs"]/div/div[1]/div[2]/ul/li[{}]'.format(number_tabs)).click() # Move to Questions Tab
        time.sleep(1.5)
        self.driver.find_element(By.XPATH, '//button[@data-test="seeAllQuestionsButton"]').click() # See all Questions
        # Deploy all questions
        while True:
            try:
                self.driver.find_element(By.XPATH, '//button[@data-test="showMoreQuestionsButton"]').click() # Load More Questions
                time.sleep(1.5)
            except:
                break
        # Extract questions
        conteiner = self.driver.find_elements(By.XPATH, '//div[@data-test="question"]')
        questions_list = []
        for question in conteiner:
            question_data = question.find_elements(By.XPATH, './*')
            list_answers = self._get_answers(question_data[-1])
            questions_list.append((question_data[0].text, list_answers))
        self.data['questions'] = questions_list
    
    def close_driver(self):
        self.driver = self.driver.close()
    
    def print_data(self):
        for par in self.data:
            print(par)
            print(self.data[par])
            print('#'*25)

if __name__ == '__main__':
    url = 'https://www.target.com/p/apple-iphone-13-pro-max/-/A-84616123?preselect=84240109#lnk=sametab'
    target = TargetWebScrapping()

    for i in range(100):
        # Inicializate driver
        target.define_driver()

        # Get data
        target.get_data(url)

        # Close Browser
        target.close_driver()

        # Print all data
        target.print_data()