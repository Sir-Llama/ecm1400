from flask import Flask, render_template, request
import covid_news_handling
import covid_data_handler
import time_conversion
import sched
import time
import json
import logging

logging.basicConfig(filename='logging.log',format = '%(levelname)s: %(asctime)s %(message)s',level=logging.DEBUG)


app = Flask(__name__)


data_scheduler = sched.scheduler(time.time, time.sleep)
       
with open ("config.json" , 'r') as config:
    data = json.load(config)
title =  data["Title"]
areaName = data["areaName"]

update_dict = {}
updatecontent = []

update_times = {}

scheduled_updates = [update_dict]

def when_to_update():
    """ function that returns the time difference in seconds """
    update_time_in_sec = time_conversion.time_difference(update_times['update_time'])
    # print(update_time_in_sec)
    return update_time_in_sec


@app.route("/index")
def index_call():
    
    data_scheduler.run(blocking = False)
    
    """ add inputed update label into dictionary """
    text_field = request.args.get('two')
    if text_field:
        logging.info("new update scheduled")
        update_dict['title'] = text_field
    update_dict["content"] = updatecontent


    """ returns time until update in seconds """
    update_time = request.args.get('update')
    if update_time != None:
        updatecontent.append(" Time will update in:" + update_time)
        update_times['update_time'] = update_time
        when_to_update()

    repeat = request.args.get('repeat')
       
    def schedule_covid_updates(update_interval=int, update_name=str):
        """Function to schedule the updates for the covid data displayed, and to routinely update if asked to repeat"""
        e1 = (update_interval , 1 , covid_data_handler.covid_API_request())
        if repeat == "repeat":
            logging.info("repeating updates every 24 hours")
            data_scheduler.enter(update_interval, 2, lambda: schedule_covid_updates(24 * 60 * 60, update_name))

  

    def schedule_news_updates(time=int):
        """Function to schedule the time until the news should be updated"""
        e1 = (time , 1 , covid_news_handling.news_API_request())


    covid_data_req = request.args.get('covid-data')
    if covid_data_req:
        schedule_covid_updates(when_to_update(),update_dict['title'])
        updatecontent.append("Covid data update requested")


    news_update = request.args.get('news')
    if news_update:
        schedule_news_updates(when_to_update())
        updatecontent.append("News update requested")

    news_articles = covid_news_handling.news_API_request()
    exeter_7_rate = covid_data_handler.covid_API_request()['Exeter_7_rate']
    england_7_rate = covid_data_handler.covid_API_request()['England_7_rate']
    hospCases = covid_data_handler.covid_API_request()['England_Hospitalisations']
    deathsTotal = covid_data_handler.covid_API_request()['England_Deaths']

    return render_template ("index.html" , 
    title = title , 
    news_articles = news_articles, 
    updates = scheduled_updates,
    location = areaName,
    local_7day_infections = exeter_7_rate,
    nation_location = 'England',
    national_7day_infections = england_7_rate,
    hospital_cases = hospCases,
    deaths_total = deathsTotal
    
    
    )

if __name__ == "__main__":
    app.run(debug=True)


