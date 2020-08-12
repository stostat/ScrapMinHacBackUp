from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
from PIL import Image
import pytesseract
import sys 
from pdf2image import convert_from_path 
import os 
import numpy as np
import json
from ClassScrapper import baseScrapper


class minhacienda(baseScrapper):
    url = 'https://www.minhacienda.gov.co/webcenter/portal/EntOrdenNacional/pages_presupuestogralnacion/presemerCOVID19'
    
        
    def scrapper(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1420,1080')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--enable-javascript')
        chrome_path = r'/snap/bin/chromium.chromedriver'
        '''
        Scrapper: this method has the main functionality of do a request with selenium throw the web page
        of minhacienda.

        1.) do a request to the page with web drive of firefox
        2.) found the numbers over the table 1..2...3..4  tag = a.x1cn
        3.) got the links for download the PDF with regex '^(T:dclay).*(pad1:)(\d*).*(goLink1)$'
        4.) feed the dictionary with the links and tags of the PDF links
        3.) then find a next page arrow (>) of table to change the page tag= tagarrownext
        4.) this is repeated the number of times that should find in the 1 step

        '''
        tagnumberofpage = 'a.x1cn'
        tagarrownext = 'a.x1cq'
        regexTaglinksPdf = re.compile(r'^(T:dclay).*(pad1:)(\d*).*(goLink1)$')
        driver = webdriver.Chrome(chrome_path, options=options)
        dictPDFs = dict()
        driver.get(self.url)
        tagsNum = driver.find_elements_by_css_selector(tagnumberofpage)
        try:
            for _ in range(len(tagsNum)+1):
                soup = BeautifulSoup(driver.page_source, 'html5lib')
                Pdflinks = soup.find_all('a', {'id': re.compile(regexTaglinksPdf)})
                for link in Pdflinks:
                    dictPDFs[str(link.get('title'))] = str(link.get('href'))
                target = driver.find_element_by_css_selector(tagarrownext)
                driver.execute_script("arguments[0].scrollIntoView();", target)
                target.click()
            driver.close()
        except Exception as e:
            print("Error: i cant find a new page, please reload the script")
            print(e)
        return dictPDFs



if __name__ == "__main__":
    scrap = minhacienda()
    pdfs = scrap.scrapper()
    scrap.gotPDFs(pdfs)
