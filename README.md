# weatherApp
Subscribes to APIs from openweathermap.com and saves 5 day 3 hour forecasts and current weather forecasts for different cities as separate collections within a MongoDB Database. This database is then used by 2 different python flask apps with a REST API-- one of them uses it to post current weather to a web app and the other uses the 5day-3hour forecast to generate a graph of the temperature forecasts for a particular city.