# weatherApp
Subscribes to APIs from openweathermap.com and saves 5 day 3 hour forecasts and current weather forecasts for different cities as separate collections within a MongoDB Database. This database is then used by 2 different python flask apps with a REST API-- one of them uses it to post current weather to a web app and the other uses the 5 day 3 hour forecast to generate a graph of the temperature forecasts for a particular city displayed on another web app.

----------------------------------------------------------------------------------------------------------------------------------------

This program has 2 parts to it:
1. Subscribing to the APIs from openweathermap.com, extracting the weather forecasts and saving the data to a MongoDB Database.(weatherDB.py)
2. Displaying this on a web app with a RESTFul API built using Python and Flask.(weatherApp.py and weatherChartApp.py)

----------------------------------------------------------------------------------------------------------------------------------------

Installation:
In addition to cloning this repository, download the following packages:-
1. MongoDB.
2. pymongo.
3. flask.
4. werkzeug
5. requests.
6. configparser
7. json.
8. threading

----------------------------------------------------------------------------------------------------------------------------------------

How to use this repository:

1. Go to openweathermap.com and get an API key.

2. Modify the config.ini file to change the API key to the one you just got and the city names, respective country codes and frequency (i.e: the number of times the database is generated every minute. The idea behind having this is that parameters like current weather are subject to change over time, so it is better to have the database get refreshed or updated with new, more recent values.) to those of your choice.

3. Navigate to the folder where MongoDB has been installed and fire up mongod.exe and mongo.exe in that order.

4. Run weatherDB.py on one terminal as python weatherDB.py. This starts up 2 separate threads running parallely-- one getting and saving 5 day 3 hour forecasts and the other doing the same for current weather. You will also see alerts being posted to the terminal in case of rain, snow or freezing temperatures(<=2 degree Fahrenheit).

5. If you want to see the weather for the cities in your config file on a web app, in another terminal run python weatherApp.py. Then go to your web browser and post http://127.0.0.1:5000/curr to it.

6. If you want to see the 5 day 3hour temperatures for any city of your choice as a graph, in a new terminal, run python weatherChartApp.py. Then go to your browser and  post http://localhost:8080/chart/city_of_your_choice to it.

