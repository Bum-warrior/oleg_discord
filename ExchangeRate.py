import requests
from bs4 import BeautifulSoup

dollar_rub = 'https://www.google.com/search?client=opera-gx&q=доллар+к+рублю&sourceid=opera&ie=UTF-8&oe=UTF-8'
euro_rub = 'https://www.google.com/search?client=opera-gx&sxsrf=ALeKk01rS0osJZuacezwDF_erndsvbIJTQ%3A1603625509675&ei=JWKVX4PXKOT2qwGKmpLgDQ&q=евро+к+рублю'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206'}

def get_rate(url,headers=headers):
    full_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.find_all(class_="DFlfde SwHCTb")
    return convert[0].text
