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
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)

    # driver = webdriver.Chrome(chrome_options=chrome_options)

    # driver = webdriver.Chrome()
    # acessar o site Vivareal
    driver.get('https://www.vivareal.com.br/')

    time.sleep(2)

    return driver


def select_purpose(driver, purpose):
    # Selecionar Alugar
    # alugar = 'rent'
    # compra = 'sale'

    select_element01 = driver.find_element(By.CLASS_NAME, 'js-select-business')
    select_object01 = Select(select_element01)
    select_object01.select_by_value(purpose)

    time.sleep(2)

def select_type(driver, type):
# Selecionar Casa
    if type == "Casa":
        type_ = 'HOME|UnitSubType_NONE,SINGLE_STOREY_HOUSE,VILLAGE_HOUSE,KITNET|RESIDENTIAL|HOME'
    elif type == "Apartamento":
        type_ = 'APARTMENT|UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX|RESIDENTIAL|APARTMENT'

    select_element02 = driver.find_element(By.CLASS_NAME, 'js-select-type')
    select_object02 = Select(select_element02)
    select_object02.select_by_value(type_)

    time.sleep(2)

def select_location(driver, location):
    # Bairro a ser procurado
    # bairro = 'moema'
    # location = 'hortolandia, são paulo'
    # full_address = bairro + ', São Paulo - SP'

    select_element03 = driver.find_element(By.CLASS_NAME, 'js-input')
    select_element03.send_keys(location)

    time.sleep(2)

    driver.implicitly_wait(5)

    search_bairro = driver.find_element(By.CLASS_NAME, 'js-location-name')
    search_bairro.click() 

def get_data(driver):

    # Dataframe to be Filled
    df_final = pd.DataFrame()

    # Get Page Content
    resp = driver.page_source
    soup = BeautifulSoup(resp, 'html.parser')

    # Get URL of each advertisement
    lista_anuncio = []
    for link in soup.find_all('a'):
        url_anuncio = link.get('href')
        if url_anuncio != None and '/imovel/' in url_anuncio:
            lista_anuncio.append(url_anuncio)
    lista_anuncio = list(set(lista_anuncio))
    # print(lista_anuncio)

    url = 'https://www.vivareal.com.br'

    # Acessando cada anuncio e extraindo informações
    for i in lista_anuncio:
         # listas vazias
        list_endereco = []
        list_area = []
        list_quartos = []
        list_banheiro = []
        list_vaga_garagem = []
        list_valor_aluguel = []
        list_valor_cond = []
        list_caracteristicas = []
        list_id_anuncio = []
        list_fonte = []
        
        dict_aux = {}
        
        link_anuncio = url+i
        
        # Getting HTML
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        req = Request(link_anuncio, headers = header)
        page = urlopen(req)
        soup = BeautifulSoup(page)
        
        # Getting data
        # try:
        endereco = soup.find('p', class_='title__address js-address')
        endereco = endereco.get_text().strip() if endereco else "sem endereco"
        
        area = soup.find('li', class_='features__item features__item--area js-area')
        area = area.get_text().strip() if area else "sem metragem"
        
        quartos = soup.find('li', class_='features__item features__item--bedroom js-bedrooms')
        quartos = quartos.get_text().strip() if quartos else "sem informacao"
        
        banheiro = soup.find('li', class_='features__item features__item--bathroom js-bathrooms')
        banheiro = banheiro.get_text().strip() if banheiro else "sem informacao"
        
        vaga_garagem = soup.find('li', class_='features__item features__item--parking js-parking')
        vaga_garagem = vaga_garagem.get_text().strip() if vaga_garagem else "sem informcao"
        
        valor_aluguel = soup.find('h3', class_='price__price-info js-price-rent')
        valor_aluguel = valor_aluguel if valor_aluguel != None else soup.find('h3', class_='price__price-info js-price-sale')         
        valor_aluguel = valor_aluguel.get_text().strip() if valor_aluguel else "sem informcao"
        
        valor_cond = soup.find('span', class_='price__list-value condominium js-condominium')
        valor_cond = valor_cond.get_text().strip() if valor_cond else "sem informacao"
        
        caracteristicas = soup.find('ul', class_='amenities__list')
        caracteristicas = caracteristicas.get_text().strip().replace('   ', ', ') if caracteristicas else "sem informacao"
        
        id_anuncio = re.search(r'\d+.$', link_anuncio).group(0).replace('/', '')
        
        fonte = link_anuncio
        # except:
        #     pass
        
        # append listas para criar dataframe
        list_endereco.append(endereco)
        list_area.append(area)
        list_quartos.append(quartos)
        list_banheiro.append(banheiro)
        list_vaga_garagem.append(vaga_garagem)
        list_valor_aluguel.append(valor_aluguel)
        list_valor_cond.append(valor_cond)
        list_caracteristicas.append(caracteristicas)
        list_id_anuncio.append(id_anuncio)
        list_fonte.append(fonte)
        
        dict_aux = {
            'endereco': list_endereco,
            'area': list_area,
            'quartos': list_quartos,
            'banheiros': list_banheiro,
            'vaga_garagem': list_vaga_garagem,
            'valor_aluguel': list_valor_aluguel,
            'valor_cond': list_valor_cond,
            'caracteristicas': list_caracteristicas,
            'id_anuncio': list_id_anuncio,
            'fonte': list_fonte
        }
        
        
        df_final = pd.concat([df_final, pd.DataFrame(dict_aux)]).reset_index(drop=True)
        time.sleep(2)

    return df_final

def click_next_page(driver):
    scroll_down = driver.find_element(By.XPATH, '//*[@id="js-site-main"]/div[2]/section[1]/div[1]/h2')
    webdriver.ActionChains(driver).move_to_element(scroll_down).perform()

    next_page = driver.find_element(By.XPATH, '//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/a')
    time.sleep(1)
    next_page.click()  
    
    return None
    
# Getting the Driver
driver = main_site()

# ==================================
# ===== FILTERS TO BE APPLIED ======
# ==================================
# Purpose -> 'rent' or 'sale'
select_purpose(driver, 'sale')

# Type = "Apartamento" or "Casa"
select_type(driver, 'Apartamento')

# Location = Bairro/Cidade
select_location(driver, 'São Paulo - SP')

df_final = pd.DataFrame()
while True:
    try:
        # Getting Data From Advertisement of a single page
        df_aux = get_data(driver)

        # concat with final dataframe
        df_final = pd.concat([df_final, df_aux]).reset_index(drop=True)
                
        click_next_page(driver)

        time.sleep(1.5)
        
    except:
        break

df_final.to_csv('df_webscraped.csv')