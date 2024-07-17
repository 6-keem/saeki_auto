import time
import subprocess
import random 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from secrets_manager import get_secret_key
import datetime
import pyperclip

class NaverAccount():
    def __init__(self) -> None:
        self.__id : str = get_secret_key(key = 'naver_id')
        self.__pw : str = get_secret_key(key = 'naver_pw')
        self.__payment_pw : str = get_secret_key(key = 'payment_pw')
    @property
    def id(self) -> str :
        return self.__id
    @property
    def pw(self) -> str :
        return self.__pw
    @property
    def payment_pw(self) -> str :
        return self.__payment_pw
    
class Saeki():
    def __init__(self) -> None:
        self.__product_link : str = get_secret_key(key = 'product_link')
        self.__saeki_id : str = get_secret_key(key = 'saeki_id')
        self.__saeki_pw : str  = get_secret_key(key = 'saeki_pw')
    @property
    def id(self) -> str :
        return self.__saeki_id
    @property
    def pw(self) -> str :
        return self.__saeki_pw
    @property
    def product_link(self) -> str :
        return self.__product_link

class MyWebdriver():
    def __init__(self):
        subprocess.Popen([
            '~/Library/Application Support/Google/Chrome',
            '--remote-debugging-port=9222',
            '--user-data-dir=/Users/keem/Library/Application Support/Google/Chrome',
            '--headless',
            '--disable-gpu'
        ])
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        self.driver = webdriver.Chrome(options = options)
        self.driver.maximize_window()
        self.all_window_handles = self.driver.window_handles
    
    def login_naver(self, naver_account : NaverAccount):
        self.all_window_handles = self.driver.window_handles
        self.driver.get('https://nid.naver.com/nidlogin.login')
        self.window_naver = [i for i in self.driver.window_handles if i not in self.all_window_handles]
        self.all_window_handles = self.driver.window_handles

        self.driver.implicitly_wait(10)
        count : int = 0
        while 'login' in self.driver.current_url:
            if count == 5:
                raise Exception('로그인에 실패하였습니다.')
            pyperclip.copy(naver_account.id)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="id"]'))
            )
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('a').send_keys('v').key_up(Keys.CONTROL).perform()

            pyperclip.copy(naver_account.pw)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="pw"]'))
            )
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('a').send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(1)

            keep = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="keep"]'))
            )
            if str(keep.get_attribute('value')) == 'off':
                keep.click()
            
            WebDriverWait(self.driver,10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="log.login"]'))
            ).click()
            time.sleep(random.uniform(0.5, 1.5))
            count += 1

    def login_saeki(self, saeki_account : Saeki):
        self.all_window_handles = self.driver.window_handles
        self.driver.get('https://www.saeki.co.kr/member/auth/login')
        self.window_saeki = [i for i in self.driver.window_handles if i not in self.all_window_handles]
        self.all_window_handles = self.driver.window_handles

        self.driver.implicitly_wait(10)
        count : int = 0
        while 'login' in self.driver.current_url:
            if count == 5:
                raise Exception('로그인에 실패하였습니다.')
            pyperclip.copy(saeki_account.id)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="loginId"]'))
            )
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('a').send_keys('v').key_up(Keys.CONTROL).perform()

            pyperclip.copy(saeki_account.pw)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="loginPw"]'))
            )
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('a').send_keys('v').key_up(Keys.CONTROL).perform()
            
            WebDriverWait(self.driver,10).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="log.login"]'))
            ).click()
            time.sleep(random.uniform(0.5, 1.5))
            count += 1

    def check_stock(self) -> bool :
        self.driver.implicitly_wait(100)
        try :
            WebDriverWait(self.driver,0.3).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="btnBuyNow"]'))
            ).click()
            print(f'🚨 {datetime.datetime.now()} : 재입고 되었습니다. 🚨')
            return True
        except TimeoutException | NoSuchElementException as e :
            print(f'{datetime.datetime.now()} : 재입고 되지 않았습니다.')
            return False
    
    def purchase_saeki(self):
        while 'orderSheet' not in self.driver.current_url:
            while self.check_stock != False:
                time.sleep(random.uniform(0.2,0.4))
                
            #TODO 다른 페이지로 넘어갈 때 url 바뀌는 시간 확인 필요
            time.sleep(random.uniform(1,2))
            self.driver.implicitly_wait(100)
        
        WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="payDiv"]/div/div[1]/div[2]/div[3]/label'))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="payAmtDiv"]/div[2]/div/label'))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="payBtn"]'))
        ).click()

    def payment_naver(self):
        #TODO switch_to.window(naver payment dialog) -> payment -> ocr 🔥
        pass
