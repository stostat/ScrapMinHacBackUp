from ClassScrapper import baseScrapper
from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from collections import defaultdict
import ssl
import requests
import json
import datetime
from mongoengine import *
from ClassModel import Contrato

class PortalTrans(baseScrapper):
    url='http://www.pte.gov.co/WebsitePTE/AQuienSeContrataSectorCovid'
    # check this two diferent endpoints
    #url='http://www.pte.gov.co/WebsitePTE/AQuienSeContrataSectorPandemia'
    # import chrome options for webdriver
    

    def scrapper(self, entitiesdict=defaultdict(list)):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_path = r'/snap/bin/chromium.chromedriver'
        regexTaglinks = re.compile('^A(q|Q).*(s|S).*(C|c).*(SectorEntidad)')
        firstIteration = False
        regexTagPagination = re.compile(r"^(javascript:)(.+)'(Page\$)(\d*)'\)$")
        if len(entitiesdict.keys()) == 0:
            urls = 1
            firstIteration = True
        else:
            listurl = list(entitiesdict.values())
            urls = len(listurl)
        for indexurldriver in range(urls):
            driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
            if len(entitiesdict.keys()) == 0:
                driver.get(self.url)
            else:
                print(listurl[indexurldriver][0])
                driver.get(listurl[indexurldriver][0])
            soup = BeautifulSoup(driver.page_source,'html5lib')
            paginationtags = soup.find_all('a', {'href': regexTagPagination})
            for index in range(len(paginationtags)+1):
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source,'html5lib')
                pages = driver.find_elements_by_xpath('//tr[@class="pagination-ys"]/td/table/tbody/tr/td/a')
                Entitieslinks = soup.find_all('a', {'href': regexTaglinks})
                for entitie in Entitieslinks:
                    if firstIteration is True:
                        entitiesdict[entitie.contents[0]].append('http://www.pte.gov.co/WebsitePTE/' + entitie.get('href'))
                    else:
                        entitiesdict[list(entitiesdict.keys())[indexurldriver]].append('http://www.pte.gov.co/WebsitePTE/' + entitie.get('href'))
                if len(pages) > index:
                    driver.execute_script("arguments[0].scrollIntoView();", pages[index])
                    driver.execute_script("arguments[0].click();", pages[index])
            driver.close()
        return entitiesdict

    def choice(self, dictlinks):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_path = r'/snap/bin/chromium.chromedriver'
        regexTaglinks = re.compile('^A(q|Q).*(s|S).*(C|c).*(SectorEntidad).*(Mes=)(\d.*).*')
        regexFirstlink = re.compile(r'.*(CodigoSector).*(NombreSector).*')
        regexTagPagination = re.compile(r"^(javascript:)(.+)'(Page\$)(\d*)'\)$")
        finishdict = defaultdict(list)
        patern = re.compile(r'.*(Mes=)(\d.*).*(NumeroCompromiso=)(\d.*).*(Beneficiario=).*')
        for key, links in dictlinks.items():
            for link in links:
                if (re.match(regexFirstlink, link)):
                    print(f'no hizo match: {link}')
                    continue
                elif (re.match(patern, link)):
                    finishdict[key].append(link)
                else:
                    link = link.replace(' ', '%20')
                    driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
                    driver.get(link)
                    soup = BeautifulSoup(driver.page_source, "html5lib")
                    paginationtags = soup.find_all('a', {'href': regexTagPagination})
                    print(f'{key}: {len(paginationtags)}')
                    for index in range(len(paginationtags)+1):
                        time.sleep(2)
                        soup = BeautifulSoup(driver.page_source, "html5lib")
                        pages = driver.find_elements_by_xpath('//tr[@class="pagination-ys"]/td/table/tbody/tr/td/a')
                        print(f'{key}: {len(pages)}')
                        tags = soup.find_all('a', {'href': regexTaglinks})
                        for tag in tags:
                            if (str(tag).find('self')) != -1:
                                print(f'\t{tag.contents[0]}')
                                finishdict[key].append('http://www.pte.gov.co/WebsitePTE/' + tag.get('href'))
                        if len(pages) > index:
                            driver.execute_script("arguments[0].scrollIntoView();", pages[index])
                            driver.execute_script("arguments[0].click();", pages[index])
                    driver.close()
        return finishdict

    def finishtable(self, dictlinks):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_path = r'/snap/bin/chromium.chromedriver'
        connect('ContratosCovid', host='localhost', port=27017)
        args = list()
        for key,links in dictlinks.items():
            for link in links:
                driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html5lib')
                lilist = soup.find('ul', {'class': 'details-info-list'})
                datalist = lilist.find_all('li')
                for data in datalist:
                    args.append(str(data.contents[2]).strip())   
                table = soup.find('table',{'class': 'table table-striped table-hover table-bordered'})
                datatable = table.find_all('td')
                for data in datatable:
                    args.append(str(data.contents[0]).strip())
                print(args)
                con = Contrato(
                    Ano = args[0],
                    Sector = key,
                    Entidad = args[1],
                    Beneficiario = args[2],
                    CodigoSubUnidad = args[3],
                    NombreSubUnidad = args[4],
                    NumerodeCompromiso = args[5],
                    TipodeDocumentoSoporte = args[6],
                    NumerodeDocumentoSoporte = args[7],
                    ObjetodelContrato = args[8],
                    RubrodelGasto = args[9],
                    ValorDelCompromiso = args[10]  
                )
                con.title = key
                con.save()
                print('element is saved in data base')
                time.sleep(2)
                driver.close()
if __name__ == '__main__':
    start_time = datetime.datetime.now()
    scrap = PortalTrans()
    #dictprimary1 = scrap.scrapper()
    #dictenti2 = scrap.scrapper(dictprimary1)
    #scrap.jsonfile(dictenti2)
    with open('decretos.json','r') as fd:
        dictenti2 = json.loads(fd.read())
    result = scrap.choice(dictenti2)
    scrap.jsonfile(result)
    #scrap.finishtable(dictenti2)
    #scrap.checkWithTxt(result)
    