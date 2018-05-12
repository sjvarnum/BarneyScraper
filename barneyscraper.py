from bs4 import BeautifulSoup
import requests
import pandas as pd


agent = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
)

pages = '96'
page = ''
url_params = {'recordsPerPage': pages, 'page': page}
base_url = 'https://www.barneys.com'
sub_url = '/category/new-arrivals/N-fh7reaZ1109flh'
url = f'{base_url}{sub_url}'

r = requests.get(url, params=url_params, headers={'User-Agent': agent})
c = r.content
soup = BeautifulSoup(c, 'html.parser')
all = soup.find_all('div', {'class': 'product-tile'})
max_page = soup.find('input', attrs={'id': 'currentPageNumber'}).get('max')


def main():
    my_list = []
    for page in range(1, int(max_page) + 1, 1):
        page_url = url + str(page)
        r = requests.get(page_url, headers={'User-Agent': agent})
        c = r.content
        soup = BeautifulSoup(c, 'html.parser')
        all = soup.find_all('div', {'class': 'product-tile'})

        for item in all:
            my_dict = {}
            try:
                my_dict['ProductID'] = (
                    item.find('input', {'class': 'product-id'}).get('value')
                )
            except AttributeError:
                None
            try:
                my_dict['ProductName'] = (
                    item.find('div', {'class': 'product-name'}).text.strip()
                )
            except AttributeError:
                None
            try:
                my_dict['ProductPrice'] = (
                    item.find('div',
                              {'class': 'product-standard-price'}).text.strip()
                )
            except AttributeError:
                None
            try:
                for link in item.find_all('a', {'class': 'brand-link'}):
                    link = link['href']
                    my_dict['ProductLink'] = f'{base_url}{link}'
            except AttributeError:
                None
            my_list.append(my_dict)
        return my_list


if __name__ == '__main__':
    data = main()
    df = pd.DataFrame(data)
    df.to_csv('new_arrivals_at_barneys_com.csv', index=False)
