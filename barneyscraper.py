from bs4 import BeautifulSoup
import requests
import pandas as pd


def requestor():

    agent = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    )

    item_cnt = '96'
    page_nbr = ''
    url_params = {'recordsPerPage': item_cnt, 'page': page_nbr}
    base_url = 'https://www.barneys.com'
    sub_url = '/category/new-arrivals/N-fh7reaZ1109flh'
    url = f'{base_url}{sub_url}'

    r = requests.get(url, params=url_params, headers={'User-Agent': agent})
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    return agent, base_url, soup, url, url_params


def get_max_page_nbr():

    agent, base_url, soup, url, url_params = requestor()
    max_page_nbr = soup.find('input',
                             attrs={'id': 'currentPageNumber'}).get('max')
    return max_page_nbr


def get_products():

    agent, base_url, soup, url, url_params = requestor()
    products = soup.find_all('div', {'class': 'product-tile'})
    return products


def main():
    agent, base_url, soup, url, url_params = requestor()
    max_page = get_max_page_nbr()
    products = get_products()

    product_list = []
    for page in range(1, int(max_page) + 1, 1):

        for item in products:
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
            product_list.append(my_dict)

    return product_list


if __name__ == '__main__':
    data = main()
    df = pd.DataFrame(data)
    print(f'Items Retrieved: {len(df.index)}')
    df.to_csv('new_arrivals_at_barneys_com.csv', index=False)
