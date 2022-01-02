import requests
import logging
import json

with open ("config.json" , 'r') as config:
    data = json.load(config)
api_key = data["apiKey"]


logging.basicConfig(filename='logging.log',format = '%(levelname)s: %(asctime)s %(message)s',level=logging.DEBUG)



def news_API_request(covidterms = "Covid Covid-19 Coronavirus"):
    """Function to request news articles filtereing for those with covid terms in the title"""

    base_url = "https://newsapi.org/v2/top-headlines?"
    country = "gb"
    complete_news_url = base_url + "country=" + country + "&apiKey=" + api_key
    
    """if the api request does not work, try changing to the backup api key """
    # api_key_backup = "b738c4b3ab7f4a0bac577fce72c0cb88"
    # complete_news_url = base_url + "country=" + country + "&apiKey=" + api_key_backup
    
    try:
        response = requests.get(complete_news_url)  
        news_response = response.json()
        articles = news_response["articles"]
        logging.info("News API request")
    except:
        logging.error("Unsuccessful news api request")

    covid_news = []
    covid_news_content = []

    """Appending content from the API to lists"""
    for article in articles:
        titles = article['title']
        newsContent = article['content']
        if 'Covid' in titles or 'Coronavirus' in titles or 'Covid-19' in titles:
            covid_news.append(titles)
            covid_news_content.append(newsContent)
    
    """list of news article in a dictionary, which will be displayed on the website"""
    news_arts = []
    for x in covid_news:
        for y in covid_news_content:
            title_content = dict(title = x , content = y)
        news_arts.append(title_content)
    # print(news_arts)

    return news_arts
