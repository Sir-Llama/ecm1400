import csv
import requests 
import logging
import sched
import time
import json

logging.basicConfig(filename='logging.log',format = '%(levelname)s: %(asctime)s %(message)s',level=logging.DEBUG)



def parse_csv_data(file_name):
    """appending csv data to a list that'll be iterated over in process_covid_csv_data"""
    temp_csv_list = []
    with open('{}'.format(file_name), 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            temp_csv_list.append(",".join(line))

    return temp_csv_list


def process_covid_csv_data(processed_data):

    hospital_cases, cumulative_deaths, last_7_days = "", "", ""
    commas = 0
    commass=0


    """hospital cases"""
    for character in processed_data[1]:
        if character == ',':
            commas += 1
        elif commas == 5:
            hospital_cases += character
    # print('hospCases:' , hospital_cases)

    """cumualtive deathes"""
    for character in processed_data[14]:
        if character == ',':
            commass += 1
        elif commass == 4:
            cumulative_deaths += character
    # print('cumDeaths: ' , cumulative_deaths)

    """7 day sum"""
    a= (processed_data[3:10])
    ab=0
    newCaseList=[]
    while ab < len(a):
        for abc in a:
            split_csv= a[ab].split(',')
            new_cases_raw = split_csv[6]
            newCaseList.append(new_cases_raw)
        ab = ab +1
    newCaseList = list(dict.fromkeys(newCaseList))
    CSVtoSum = [int(i)for i in newCaseList]
    last_7_days = sum(CSVtoSum)
    # print('last_7_days:' , last_7_days)

    return  int(last_7_days), int(hospital_cases), int(cumulative_deaths)

process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))

with open ("config.json" , 'r') as config:
    data = json.load(config)
areaType =  data["areaType"]
areaName = data["areaName"]

base_url =          'https://api.coronavirus.data.gov.uk/v1/data?'
exeter_filter =     'filters=areaType=' + areaType + ';areaName=' + areaName + "&"
england_filter =    'filters=areaType=nation;areaName=england&'
structure =         'structure={"newCases":"newCasesByPublishDate","hospitalCases":"hospitalCases","cumDeaths28DaysByPublishDate":"cumDeaths28DaysByPublishDate"}'

complete_url_exeter = base_url + exeter_filter + structure
complete_url_england = base_url + england_filter + structure

def covid_API_request(location = 'exeter', locationtype = 'ltla'):
    """Function to gather data from UK Covid API"""


    logging.info("Covid data API Request")

    """ Gathering API data for Exeter """
    try:
        ExeterDetails = requests.get(complete_url_exeter).json()
    except:
        logging.error("Unsuccessful exeter covid data request")
        
    newcases_exeter = []
    day = 0

    for block in ExeterDetails["data"]:
        newcases_exeter.append(block["newCases"])
        day += 1
        if day == 7:
            break
    
    """ Gathering API data for England """
    try:
        EnglandDetails = requests.get(complete_url_england).json()
    except:
        logging.error("Unsuccessful England covid data request")

    england_newcases = []
    hosp_england = []
    deaths_england = []
    dayy = 0

    for block in EnglandDetails["data"]:
        england_newcases.append(block["newCases"])
        dayy += 1
        if dayy == 7:
            break

    for block in EnglandDetails["data"]:
        deaths_england.append(block["cumDeaths28DaysByPublishDate"])
        break

    for block in EnglandDetails["data"]:
        if block["hospitalCases"] is None:
            pass
        else:
            hosp_england.append(block["hospitalCases"])
            break

    eng_7_rate = (sum(england_newcases))
    ex_7_rate = (sum(newcases_exeter))

    for i in deaths_england:
        eng_deaths = i
    for i in hosp_england:
        eng_hosps = i

    """ Returning processed data in a dictionary """
    finaldict = {}
    finaldict['Exeter_7_rate'] = ex_7_rate
    finaldict['England_Deaths'] = eng_deaths
    finaldict['England_Hospitalisations'] = eng_hosps
    finaldict['England_7_rate'] = eng_7_rate

    # print(finaldict)    
    return finaldict


