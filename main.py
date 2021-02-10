import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlopen


def lista_leis():
    """
    Lista todas as leis existentes no site para o dominio acima citado
    """
    option = Options()
    option.headless = True
    driver = webdriver.Firefox(options=option)
    # driver = webdriver.Firefox()

    pagina_legislacao = "https://www.juazeirodonorte.ce.gov.br/legislacao/?p="
    numero_da_pagina = 1
    leis = []
    while True:
        url = f"{pagina_legislacao}{numero_da_pagina}"
        print(f'Página: {numero_da_pagina}')
        driver.get(url)
        time.sleep(2)

        try:
            elemento = driver.find_element_by_xpath(
                '/html/body/div/section/div/div[2]/div[1]/div/div/table/tbody/tr')
        except NoSuchElementException:
            print("Não encontrada publicações nesta página => Última página!")
            break
        else:
            numero_por_pagina = len(driver.find_elements_by_xpath("/html/body/div/section/div/div[2]/div[1]/div/div/table/tbody/tr"))
            print(f' |- {numero_por_pagina} publicações encontradas na página.')

            numero_da_pagina += 1
            for lei_por_pagina in range(1, numero_por_pagina + 1):
                texto_lei = driver.find_element_by_xpath(
                    f"/html/body/div/section/div/div[2]/div[1]/div/div/table/tbody/tr[{lei_por_pagina}]/td[1]/a").text
                url_lei = driver.find_element_by_xpath(
                    f"/html/body/div/section/div/div[2]/div[1]/div/div/table/tbody/tr[{lei_por_pagina}]/td[1]/a").get_attribute(
                    "href")
                lei = [texto_lei, url_lei]
                leis.append(lei)
        print("- - - - - -")

    return leis

def procura_lei(leis):
    '''
    Procura leis e decretos com as palavras contidas na lista palavras
    '''
    palavras = ['ppdu', 'plano', 'diretor', 'plano diretor', 'luos', 'uso', 'ocupação', 'solo', 'parcelamento', 'lei de uso', 'planta', 'cop', 'obra', 'código de obra', 'obra e postura', 'postura', '2569', '2570', '2571', '2572']
    leis_filtradas = []
    cont = 1
    for lei in leis:
        texto_lei = lei[0]
        texto_lei = texto_lei.lower()
        operador = 0
        for palavra in texto_lei.split(' '):
            if palavra in palavras:
                operador = 1
        if operador == 1:
            leis_filtradas.append(lei)
        print(f"{cont} analisada(s)")
        cont += 1

    print(leis_filtradas)
    return leis_filtradas

def download_file(leis_filtradas):
    """
    Realiza dos downloas das legislações
    """
    for lei in leis_filtradas:
        url = lei[1]
        response = urlopen(url)
        with open(f"{lei[0]}.pdf", 'wb') as file:
            file.write(response.read())
            print("PDF salvo!!!")

    print("SCRAPING CONCLUÍDO, FINALIZANDO...")

def main():
    download_file(procura_lei(lista_leis()))

main()