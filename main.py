from fastapi import FastAPI, Path
import cloudscraper
from bs4 import BeautifulSoup

app = FastAPI()
scraper = cloudscraper.create_scraper(
    delay=10, browser={'custom': 'ScraperBot/1.0'})


@app.get("/")
def getData():
    return 'Hello World! This application works.'


@app.get("/stocks/{ticker}")
def getIndividualStocksData(ticker: str):

    url = f'https://finviz.com/quote.ashx?t={ticker}'
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    table_rows = soup.select('.snapshot-table2 .table-dark-row')
    temp_list = []
    result_dict = {}

    for row in table_rows:
        row_cells = row.find_all('td')

        for i in range(len(row_cells)):
            text = row_cells[i].text
            temp_list.append(text)

            if i % 2 > 0:
                result_dict[temp_list[0]] = temp_list[1]
                temp_list.clear()

    return result_dict


@app.get("/screener/overview/{exchange}")
def getScreenersOverviewData(exchange: str):
    # exchange = 'AMEX' | 'NYSE' | 'NASDAQ'

    url = f'https://finviz.com/screener.ashx?v=111&f=exch_{exchange.lower()[:4]}'
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    result_dict = {}
    headers = []

    headers_row = soup.select('.table-light tr .table-top.cursor-pointer')
    for td in headers_row:
        headers.append(td.text)

    print(headers)

    # table_rows = soup.select('.snapshot-table2 .table-dark-row')
    # temp_list = []
    # result_dict = {}

    # for row in table_rows:
    #     row_cells = row.find_all('td')

    #     for i in range(len(row_cells)):
    #         text = row_cells[i].text
    #         temp_list.append(text)

    #         if i % 2 > 0:
    #             result_dict[temp_list[0]] = temp_list[1]
    #             temp_list.clear()
    return result_dict
