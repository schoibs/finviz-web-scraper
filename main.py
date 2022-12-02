import requests
from bs4 import BeautifulSoup
import cloudscraper

ticker = 'MSFT'
scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0'})

url = f'https://finviz.com/quote.ashx?t={ticker}'
response = scraper.get(url)

soup = BeautifulSoup(response.content, 'lxml')

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

print(result_dict)