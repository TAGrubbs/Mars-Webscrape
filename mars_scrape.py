from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
def init_browser():
    executable_path = {"executable_path": "C:\Program Files\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
def scrape():
    mars_scrape={}
    browser= init_browser()
    #NewsScrape
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204%3A165&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text
    mars_scrape['news_title']=news_title
    mars_scrape['news_p']=news_p
    #ImageScrape
    image_url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html_featured_image = browser.html
    image_soup = BeautifulSoup(html_featured_image, 'html.parser')
    nasa_image_url=image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    nasa_url= 'https://www.jpl.nasa.gov'
    complete_image_url= nasa_url + nasa_image_url
    mars_scrape['complete_image_url']=complete_image_url
    #WeatherScrape
    weather_url= 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    html_weather= browser.html
    weather_soup=BeautifulSoup(html_weather, 'html.parser')
    tweets=weather_soup.find_all('div', class_='js-tweet-text-container')
    mars_weather=''
    for tweet in tweets:
        if 'InSight' in tweet.find('p').text:
            mars_weather=tweet.text
            break
        else:
            pass
    mars_scrape['mars_weather']= mars_weather
    #TableScrape
    facts_url='https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[1]
    df.columns=['Fact', 'Value']
    df.set_index('Fact', 'Value' , inplace=True)
    html_table = df.to_html()
    mars_scrape['html_table']= html_table
    #WeathereScrape
    hemispheres_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemispheres= browser.html
    hemisphere_soup=BeautifulSoup(html_hemispheres, 'html.parser')
    hemisphere_items=hemisphere_soup.find_all('div', class_='item')
    hemisphere_image_urls=[]
    hemi_main_url = 'https://astrogeology.usgs.gov'
    for i in hemisphere_items:
        title= i.find('h3').text
        hemi_img_url=i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemi_main_url+hemi_img_url)
        hemi_html=browser.html
        hemi_soup= BeautifulSoup(hemi_html, 'html.parser')
        hemi_img_url= hemi_main_url + hemi_soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({'title': title, 'img_url': hemi_img_url})
    mars_scrape['hemishphere_image_urls']=hemisphere_image_urls

    return mars_scrape
