import numpy as np
import requests, json
import ipdb
import configparser
import threading
from threading import Thread
from pymongo import MongoClient
import time

# Read the config file
parser = configparser.ConfigParser()
parser.read('config.ini')
# import pdb;pdb.set_trace()
api_key = parser['config']['api_key']
cities = parser['config']['cities'].split(", ")
country_codes = parser['config']['country_codes'].split(", ")
freq = int(parser['config']['frequency'])
date = parser['config']['date']
opacity = parser['config']['opacity']
fill_bound = parser['config']['fill_bound']

sleep_time = 60.0/freq

url_5day3hour = "http://api.openweathermap.org/data/2.5/forecast?"
# url_weathermaps = "http://maps.openweathermap.org/maps/2.0/weather/TA2/19/256/256?"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def KelvinToFahrenheit(temp):
    celc = temp-273
    fah = (9*celc/5.0)+32
    return fah

#Used to print alerts just in case there is rain/snow/freezing temperatures
def printAlerts(x_5day3hour):
    for i in range(len(x_5day3hour['list'])):
        x = x_5day3hour['list'][i]
        if x['weather'][0]['main'] == 'Rain':
            pr = "Rain in " + x_5day3hour['city']['name'] + ', ' + x_5day3hour['city']['country'] + " on " + x['dt_txt'] + "."
            print(pr)
        if x['weather'][0]['main'] == 'Snow':
            pr = "Snow in " + x_5day3hour['city']['name'] + ', ' + x_5day3hour['city']['country'] + " on " + x['dt_txt'] + "."
            print(pr)
        temp = KelvinToFahrenheit(x['main']['temp'])
        if temp<=2:
            pr = "Freezing temperatures in " + x_5day3hour['city']['name'] + ', ' + x_5day3hour['city']['country'] + " on " + x['dt_txt'] + "."
            print(pr)

#Subscribe to API for 5day3hour forecasts 5 times a minute and insert the data into a MongoDB database
def process_5day3hour():
    client = MongoClient('mongodb://localhost:27017/')
    # Using  Database Weather
    db = client.weather
    # Using  Collection five_days
    collection = db.five_days
    while(True):
        for i in range(len(cities)):
            complete_url_5day3hour = url_5day3hour + "appid=" + api_key + "&q=" + cities[i] + "," + country_codes[i]
            response_5day3hour = requests.get(complete_url_5day3hour)
            x_5day3hour = response_5day3hour.json()
            printAlerts(x_5day3hour)
            # Defining the data 
            record = {cities[i]:x_5day3hour}
            # Inserting record in the DB
            collection.insert(record)
        time.sleep(sleep_time)    

#Subscribe to API for current weather and put it in another collection of the same MongoDB database
def process_current():
    client = MongoClient('mongodb://localhost:27017/')
    # Using  Database Weather
    db = client.weather
    # Using  Collection five_days
    collection = db.current_data
    while(True):
        for i in range(len(cities)):
            complete_url = base_url + "appid=" + api_key + "&q=" + cities[i]
            response = requests.get(complete_url)
            x = response.json()
            record = x
            # Inserting record in the DB
            collection.insert(record)
        time.sleep(sleep_time)

#Class to be used for threading
class MyThread(Thread):
 
    def __init__(self, val):
        ''' Constructor. '''
        Thread.__init__(self)
        self.val = val

    #Runs either of the 2 processes based on which thread being is called
    def run(self):
        if self.val == 1:
            process_5day3hour()
        if self.val == 2:
            process_current()

if __name__ == "__main__":
    try:
        print("Start!!")
        myThreadOb1 = MyThread(1)
        myThreadOb1.setName("Thread1")

        myThreadOb2 = MyThread(2)
        myThreadOb2.setName("Thread2")

        myThreadOb1.start()
        myThreadOb2.start()

        myThreadOb1.join()
        myThreadOb2.join()

    except IOError:
        print("Thread not working")