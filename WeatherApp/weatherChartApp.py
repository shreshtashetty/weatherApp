from flask import Flask, Markup, render_template
import configparser
import requests, json

# Read the config file
parser = configparser.ConfigParser()
parser.read('config.ini')
api_key = parser['config']['api_key']
weather_forecast_url="http://api.openweathermap.org/data/2.5/forecast?"

app = Flask(__name__)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

def kelvinToFahrenheit(temp):
    celc = temp-273
    fah = (9*celc/5.0)+32
    return fah

@app.route('/chart/<city>')
def cityWeatherChart(city):
    forecast_labels=[]
    forecast_values=[]
    
    response_5day3hour = requests.get(weather_forecast_url + "appid=" + api_key + "&q=" + city + ",US")
    city_forecast_dict = json.loads(response_5day3hour.text)
#"list":[{"dt":1578150000,"main":{"temp":272.37,"feels_like":263.6,"temp_min":272.37,"temp_max":273.04,"pressure":1016,"sea_level":1016,"grnd_level":994,"humidity":78,"temp_kf":-0.67},"weather":[{"id":600,"main":"Snow","description":"light snow","icon":"13d"}],"clouds":{"all":100},"wind":{"speed":8.94,"deg":323},"snow":{"3h":0.38},"sys":{"pod":"d"},"dt_txt":"2020-01-04 15:00:00"}
    
    i=0
    for entry in city_forecast_dict['list']:
        forecast_labels.append(entry['dt_txt'])
        forecast_values.append(kelvinToFahrenheit(entry['main']['temp']))
        i = i + 1
    
    return render_template('weather_forecast_chart.html', title='5 Day Forecast for {},US'.format(city), max=100, labels=forecast_labels, values=forecast_values)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
