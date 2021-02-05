from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import os


def scrape_title(query):
    # URL of page to be scraped

    base_url = 'https://reelgood.com'
    url = f'{base_url}/search?q={query}'

    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.select('.e1qyeclq5 a')[0]['href']
    show_url = base_url + link
    print(show_url)

    show_response = requests.get(show_url)
    show_soup = BeautifulSoup(show_response.text, 'html.parser')

    title = ''
    services = ''
    desc = ''
    feature_img = ''
    recommended = ''
    genre = ''
    rating = ''
    maturity = ''
    country = ''
    try:
        title = show_soup.select('h1.e14injhv7')[0].text
        services = show_soup.select('.e126mwsw1 span[class*=hou113]')
        desc = show_soup.select('p[itemprop=description]')[0].text
        feature_img = show_soup.select(
            '.e1x40mdt0 picture.e1181ybh0 img.e1181ybh1')[0]['src']
        recommended = show_soup.select('.e1yfir8f4 .e1qyeclq4')
        genre = show_soup.find('a', class_='css-10wrqt0').text
        rating = show_soup.find('span', class_='ey4ir3j3').text
        maturity = show_soup.select('span[title*=rating]')[0].text
        country = show_soup.select('.css-10wrqt0[href*=origin]')[0].text
    except:
        print('error')

    #Individual Search Dictionary
    dic_list = {
        'title': title,
        'services': [s.text for s in set(services)],
        'description': desc,
        'feature_img': feature_img,
        'genre': genre,
        'rating': rating,
        'maturity': maturity,
        'country': country,
        'recommended': [r.text for r in recommended]
    }
    
    
    return dic_list
