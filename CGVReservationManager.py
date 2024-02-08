from libs.selechecker import selechecker
from libs.logmanager.LogManager import LogManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import random
import datetime
import time
import os


class CGVReservationManager:
    def __init__(self):
        self.cgv_id, self.cgv_pw = '', ''
        self.input_account()
        self.loger = LogManager()
        # self.driver = webdriver.Chrome(selechecker.driver_check())
        self.driver = webdriver.Chrome()
        self.movie_dict, self.movie_element_dict = {}, {}
        self.choose_dict, self.choose_element_dict = {}, {}
        self.choose_list, self.choose_element_list = [], []
        self.backslash_enter = '\n'
        self.login()

    def __del__(self):
        self.driver.close()

    def get_element_by_xpath(self, xpath_content: str, is_print_log: bool = True) -> WebElement:
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_content))
        )
        if is_print_log:
            self.loger.update(0, f'XPATH is detected: {element}')
        return element

    def get_elements_by_xpath(self, xpath_content: str, is_print_log: bool = True) -> list[WebElement]:
        element_list = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath_content))
        )
        if is_print_log:
            self.loger.update(0, f'XPATH is detected: {element_list}')
        return element_list

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
        self.driver.switch_to.frame(self.get_element_by_xpath('//*[@id="ticket_iframe"]'))

    def get_movie_list(self):
        movie_list = []
        movie_element_list = self.get_elements_by_xpath('//*[@id="movie_list"]/ul/li')
        for movie_element in movie_element_list:
            movie_list.append(f'PG {movie_element.text.replace(self.backslash_enter, " - ")}')
        self.choose_list = movie_list
        self.choose_element_list = movie_element_list
        self.print_and_choose_from_list('Choose one of the lists below (number): ')

    def get_movie_type(self):
        movie_type_list = []
        movie_type_element_list = self.get_elements_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div[1]/div[1]'
                                                             '/div[2]/div/div[3]/ul/div/ul/li')
        for movie_type_element in movie_type_element_list:
            if movie_type_element.is_displayed():
                movie_type_list.append(movie_type_element.text)
        self.choose_list = movie_type_list
        self.choose_element_list = movie_type_element_list
        self.print_and_choose_from_list('Choose movie type of the list below (number): ')

    def get_region(self):
        region_list = []
        region_element_list = self.get_elements_by_xpath('//*[@id="theater_area_list"]/ul/li')
        for region_element in region_element_list:
            if region_element.is_displayed():
                region_list.append(f'{region_element.text.replace(self.backslash_enter, " - ", 1).replace(self.backslash_enter, ", ")}')
        self.choose_list = region_list
        self.choose_element_list = region_element_list
        self.print_and_choose_from_list('Choose theater region of the list below (number): ')

    def get_theater(self):
        theater_list = []
        theater_element_list = self.get_elements_by_xpath('//*[@id="theater_area_list"]/ul/li[2]/div/ul/li')
        for theater_element in theater_element_list:
            if theater_element.is_displayed():
                theater_list.append(theater_element.text)
        self.choose_list = theater_list
        self.choose_element_list = theater_element_list
        self.print_and_choose_from_list('Choose theater of the list below (number): ')
        loading_image = self.get_element_by_xpath('//*[@id="ticket_loading"]/p/img')
        while loading_image.is_displayed():
            continue

    def get_date(self):
        date_list = []
        date_element_list = self.get_elements_by_xpath('//*[@id="date_list"]/ul/div/li')
        new_date_element_list = []
        for date_element in date_element_list:
            if 'dimmed' not in date_element.get_attribute('class'):
                date_list.append(f'{date_element.text.replace(self.backslash_enter, " ")}일')
                new_date_element_list.append(date_element)
        self.choose_list = date_list
        self.choose_element_list = new_date_element_list
        self.print_and_choose_from_list('Choose date of the list below (number): ')
        loading_image = self.get_element_by_xpath('//*[@id="ticket_loading"]/p/img')
        while loading_image.is_displayed():
            continue

    def get_time(self):
        time_dict = {}
        time_list = []
        time_element_list = self.get_elements_by_xpath('//*[@id="ticket"]'
                                                       '/div[2]/div[1]/div[4]/div[2]/div[3]/div[1]/div')
        for time_element in time_element_list:
            refine_data = time_element.text.split(self.backslash_enter)
            refine_time_of_theater_title = refine_data[0]
            refine_time_element_text_list = refine_data[1:]
            time_dict[refine_time_of_theater_title] = []
            for i in range(len(refine_time_element_text_list) // 2):
                time_dict[refine_time_of_theater_title].append(f'{"".join(refine_time_element_text_list[i*2])} '
                                                               f'({"".join(refine_time_element_text_list[i*2+1])})')
        self.loger.update(0, f'time_dict: {time_dict}')
        self.choose_dict = time_dict
        self.choose_element_list = time_element_list
        self.print_and_choose_from_dict('Choose date of the list below (number): ')

    def print_selection_dict(self, context: str = 'Choose one of the lists below (number):') -> int:
        while True:
            count = 0
            for i in range(len(self.choose_dict.keys())):
                print(f'{list(self.choose_dict.keys())[i]}')
                for j in range(len(list(self.choose_dict.values())[i])):
                    print(f'[{count + 1}] {list(self.choose_dict.values())[i][j]}')
                    count += 1
                print()
            input_choose_num = input(context)
            try:
                input_choose_num = int(input_choose_num)
            except ValueError:
                os.system('cls')
                print(f'The value you entered is not a number: [ {input_choose_num} ]')
                print('Please enter a number.')
                continue
            return input_choose_num

    def print_and_choose_from_dict(self, context: str) -> None:
        input_choose_num = self.print_selection_dict(context)

    def print_selection_list(self, context: str = 'Choose one of the lists below (number):') -> int:
        while True:
            for i in range(len(self.choose_list)):
                print(f'[{i+1}] {self.choose_list[i]}')
                i += 1
            input_choose_num = input(context)
            try:
                input_choose_num = int(input_choose_num)
            except ValueError:
                os.system('cls')
                print(f'The value you entered is not a number: [ {input_choose_num} ]')
                print('Please enter a number.')
                continue
            return input_choose_num

    def print_and_choose_from_list(self, context: str) -> None:
        input_choose_num = self.print_selection_list(context)
        self.loger.update(0, f'고른 영화 타입: {self.choose_list[input_choose_num - 1]}')
        self.loger.update(0, f'고른 영화 타입 엘리먼트: {self.choose_element_list[input_choose_num - 1]}')
        self.choose_element_list[input_choose_num - 1].click()




