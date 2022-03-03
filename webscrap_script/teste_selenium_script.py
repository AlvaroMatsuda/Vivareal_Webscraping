import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import math
import requests

def main_site():
    driver = webdriver.Chrome()
    # acessar o site Vivareal
    driver.get('https://www.vivareal.com.br/')

    time.sleep(2)

    return driver


def select_purpose(driver):
    # Selecionar Alugar
    alugar = 'rent'
    compra = 'sale'

    select_element01 = driver.find_element(By.CLASS_NAME, 'js-select-business')
    select_object01 = Select(select_element01)
    select_object01.select_by_value(alugar) # alguar

    time.sleep(2)

def select_type(driver):
# Selecionar Casa
    casa = 'HOME|UnitSubType_NONE,SINGLE_STOREY_HOUSE,VILLAGE_HOUSE,KITNET|RESIDENTIAL|HOME'
    apartamento = 'APARTMENT|UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX|RESIDENTIAL|APARTMENT'

    select_element02 = driver.find_element(By.CLASS_NAME, 'js-select-type')
    select_object02 = Select(select_element02)
    select_object02.select_by_value(apartamento) # apartamento

    time.sleep(2)

def select_location(driver):
    # Bairro a ser procurado
    # bairro = 'moema'
    bairro = 'hortolandia'
    full_address = bairro + ', São Paulo - SP'

    select_element03 = driver.find_element(By.CLASS_NAME, 'js-input')
    select_element03.send_keys(bairro)

    time.sleep(2)

    driver.implicitly_wait(5)

    search_bairro = driver.find_element(By.CLASS_NAME, 'js-location-name')
    search_bairro.click() 



driver = main_site()

select_purpose(driver)

select_type(driver)

select_location(driver)