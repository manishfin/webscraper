from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


AMAZON = 'https://www.amazon.in'

def getItemObj(item_details):
    obj = {}
    try:
        item_divs = item_details.find('span').find('div').find('div').select_one('div div:nth-of-type(2)').findChildren('div', recursive=False)
        item_details_divs = item_divs[1].find('div').findChildren('div', recursive=False)
    except:
        return {}
    try:
        obj['img'] = item_divs[0].find('img').get('src')
        obj['link'] = AMAZON + item_divs[0].find('a').get('href')
    except:
        obj['img'] = None
        obj['link'] = None
    try:
        obj['price'] = item_details_divs[1].select('.a-price > .a-offscreen')[0].text
    except:
        obj['price'] = None
    try:
        obj['name'] = item_details_divs[0].select('h2 > a > span')[0].text
    except:
        obj['name'] = None
    try:
        obj['status'] = item_details_divs[1].find('span', attrs={'aria-label': 'Currently unavailable.'}).find('span').text
    except:
        obj['status'] = None
    return obj

def scraper(request):
    if request.method == 'POST':
        item = request.POST['item']
        search = item.split()
        search_string = "+".join(search)
        try:
            url = AMAZON+"/s?k="+search_string
            html = urlopen(url)
            soup = BeautifulSoup(html.read(), 'html.parser')
            searched_items = soup.findAll("div", attrs={"data-asin" : True})
        except:
            return render(request, 'scraper/scraper.html', {"error": 'Server is not responding! Please retry in sometime.', 'item': item})
        data = []
        for each_item_details in searched_items:  
            item_data = getItemObj(each_item_details)
            data.append(item_data)
        return render(request, 'scraper/scraper.html', {"data": data, 'item': item})
    return render(request, 'scraper/scraper.html')
