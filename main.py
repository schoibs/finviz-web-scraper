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


@app.get("/screener/overview/{exchange}/{page}")
def getScreenersOverviewData(exchange: str, page:int = 1):
    # exchange = 'AMEX' | 'NYSE' | 'NASDAQ'

    if page > 1:
        page = (page - 1) * 20 + 1

    url = f'https://finviz.com/screener.ashx?v=111&f=exch_{exchange.lower()[:4]}&r={page}'
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    result_dict = {}
    headers = []

    pagination = soup.select('.screener_pagination a')
    total_page = pagination[-1].text
    if total_page == 'next':
        total_page = pagination[-2].text

    headers_row = soup.select('.table-light tr .table-top.cursor-pointer')
    for td in headers_row:
        headers.append(td.text)

    results = []

    content_rows = soup.select('.table-light tr[valign="top"]')
    for row in content_rows:
        row_dict = {}
        td_list = row.find_all('td')

        for i in range(len(td_list)):
            row_dict[headers[i]] = td_list[i].text

        results.append(row_dict)

    result_dict['total_page'] = total_page
    result_dict['results'] = results
    return result_dict
