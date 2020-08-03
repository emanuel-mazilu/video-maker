import requests
from bs4 import BeautifulSoup


URL = 'https://www.fluentu.com/blog/english/basic-english-phrases/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='main')
job_elems = results.find('div', class_='entry')
h3_list = job_elems.find_all('h3')

for h3_elem in h3_list:
    print(h3_elem.text)