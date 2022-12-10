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

    output = {}

    # extract the website html content
    url = f'https://finviz.com/quote.ashx?t={ticker}'
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    # extract information from table by looping through each table row
    temp_list = []
    table_rows = soup.select('.snapshot-table2 .table-dark-row')
    for row in table_rows:
        row_cells = row.find_all('td')

        for i in range(len(row_cells)):
            text = row_cells[i].text
            temp_list.append(text)

            if i % 2 > 0:
                output[temp_list[0]] = temp_list[1]
                temp_list.clear()

    return output


@app.get("/screener/overview/{exchange}/{page}")
def getScreenerOverviewData(exchange: str, page:int = 1, market_cap='', sector='', index='', target_price='', p_e=''):
    output = {}

    # get the correct page representation
    if page > 1:
        page = (page - 1) * 20 + 1

    # extract the website html content
    url = f'https://finviz.com/screener.ashx?v=111&f=exch_{exchange.lower()[:4]},cap_{market_cap},sec_{sector},idx_{index},targetprice_{target_price},fa_pe_{p_e}&ft=4&r={page}'
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    # extract table headers
    headers = []
    headers_row = soup.select('.table-light tr .table-top.cursor-pointer')
    for td in headers_row:
        headers.append(td.text)

    # extract table content by looping through each table row
    results = []
    content_rows = soup.select('.table-light tr[valign="top"]')
    for row in content_rows:
        row_dict = {}
        td_list = row.find_all('td')

        for i in range(len(td_list)):
            row_dict[headers[i]] = td_list[i].text

        results.append(row_dict)

    # get total pages
    total_page = 0
    if len(headers) > 0:
        pagination = soup.select('.screener_pagination a')
        total_page = pagination[-1].text

        if total_page == 'next':
            total_page = pagination[-2].text

    output['total_page'] = total_page
    output['results'] = results
    return output


@app.get("/screener/valuation/{exchange}/{page}")
def getScreenerValuationData(exchange: str, page:int = 1, market_cap='', sector='', index='', target_price='', p_e=''):
    output = {}

    # get the correct page representation
    if page > 1:
        page = (page - 1) * 20 + 1

    # extract the website html content
    url = f'https://finviz.com/screener.ashx?v=121&f=exch_{exchange.lower()[:4]},cap_{market_cap},sec_{sector},idx_{index},targetprice_{target_price},fa_pe_{p_e}&ft=4&r={page}'
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    # extract table headers
    headers = []
    headers_row = soup.select('.table-light tr .table-top.cursor-pointer')
    for td in headers_row:
        headers.append(td.text)

    # extract table content by looping through each table row
    results = []
    content_rows = soup.select('.table-light tr[valign="top"]')
    for row in content_rows:
        row_dict = {}
        td_list = row.find_all('td')

        for i in range(len(td_list)):
            row_dict[headers[i]] = td_list[i].text

        results.append(row_dict)

    # get total pages
    total_page = 0
    if len(headers) > 0:
        pagination = soup.select('.screener_pagination a')
        total_page = pagination[-1].text

        if total_page == 'next':
            total_page = pagination[-2].text

    output['total_page'] = total_page
    output['results'] = results
    return output

@app.get("/screener/financial/{exchange}/{page}")
def getScreenerFinancialData(exchange: str, page:int = 1, market_cap='', sector='', index='', target_price='', p_e=''):
    output = {}

    # get the correct page representation
    if page > 1:
        page = (page - 1) * 20 + 1

    # extract the website html content
    url = f'https://finviz.com/screener.ashx?v=161&f=exch_{exchange.lower()[:4]},cap_{market_cap},sec_{sector},idx_{index},targetprice_{target_price},fa_pe_{p_e}&r={page}'
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    # extract table headers
    headers = []
    headers_row = soup.select('.table-light tr .table-top.cursor-pointer')
    for td in headers_row:
        headers.append(td.text)

    # extract table content by looping through each table row
    results = []
    content_rows = soup.select('.table-light tr[valign="top"]')
    for row in content_rows:
        row_dict = {}
        td_list = row.find_all('td')

        for i in range(len(td_list)):
            row_dict[headers[i]] = td_list[i].text

        results.append(row_dict)

    # get total pages
    total_page = 0
    if len(headers) > 0:
        pagination = soup.select('.screener_pagination a')
        total_page = pagination[-1].text

        if total_page == 'next':
            total_page = pagination[-2].text

    output['total_page'] = total_page
    output['results'] = results
    return output

@app.get("/screener/ownership/{exchange}/{page}")
def getScreenerOwnershipData(exchange: str, page:int = 1, market_cap='', sector='', index='', target_price='', p_e=''):
    output = {}

    # get the correct page representation
    if page > 1:
        page = (page - 1) * 20 + 1

    # extract the website html content
    url = f'https://finviz.com/screener.ashx?v=131&f=exch_{exchange.lower()[:4]},cap_{market_cap},sec_{sector},idx_{index},targetprice_{target_price},fa_pe_{p_e}&r={page}'
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")

    # extract table headers
    headers = []
    headers_row = soup.select('.table-light tr .table-top.cursor-pointer')
    for td in headers_row:
        headers.append(td.text)

    # extract table content by looping through each table row
    results = []
    content_rows = soup.select('.table-light tr[valign="top"]')
    for row in content_rows:
        row_dict = {}
        td_list = row.find_all('td')

        for i in range(len(td_list)):
            row_dict[headers[i]] = td_list[i].text

        results.append(row_dict)

    # get total pages
    total_page = 0
    if len(headers) > 0:
        pagination = soup.select('.screener_pagination a')
        total_page = pagination[-1].text

        if total_page == 'next':
            total_page = pagination[-2].text

    output['total_page'] = total_page
    output['results'] = results
    return output
