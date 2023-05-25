from libs.selechecker import selechecker
from libs.logmanager.LogManager import LogManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import datetime
import time


class CGVReservationManager:
    def __init__(self):
        self.cgv_id, self.cgv_pw = '', ''
        self.input_account()
        self.loger = LogManager()
        self.driver = webdriver.Chrome(selechecker.driver_check())
        self.login()

    def __del__(self):
        self.driver.close()

    def get_element_by_xpath(self, xpath_content: str, is_print_log: bool = True):
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_content))
        )
        if is_print_log:
            self.loger.update(0, f'XPATH is detected: {element}')
        return element

    def input_account(self):
        self.cgv_id = input('Please enter your CGV ID: ')
        self.cgv_pw = input('Please enter your CGV PW: ')

    def login(self):
        url = 'https://www.cgv.co.kr/user/login'
        return_url = 'http://www.cgv.co.kr/ticket/'
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        self.get_element_by_xpath('//*[@id="txtUserId"]').send_keys(self.cgv_id)
        self.get_element_by_xpath('//*[@id="txtPassword"]').send_keys(self.cgv_pw)
        self.get_element_by_xpath('//*[@id="submit"]/span').click()
        while self.driver.current_url == url:
            continue
        self.driver.get(return_url)

    def get_movie_list(self):
        limit_age = self.get_element_by_xpath('//*[@id="movie_list"]/ul/li[1]/a/i').text
        movie_name = self.get_element_by_xpath('//*[@id="movie_list"]/ul/li[1]/a/span[1]').text
        # '//*[@id="movie_list"]/ul/li[2]/a/span[1]'
        self.loger.update(0, f'limit_age: {limit_age}')
        self.loger.update(0, f'movie_name: {movie_name}')

