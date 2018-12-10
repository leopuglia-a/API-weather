API_KEY = 'a31d9ea1bdc6a01f8413f8da791f08e9'
URL = 'http://api.openweathermap.org/data/2.5/weather?'
CITY_NAME = 'Maringá'
CITY_ID = '6322863'
UNITS = 'metric'

import urllib.request
import json
import datetime
import serial
import time

def urlBuild():
    return URL + '&id=' + str(CITY_ID) + '&units=' + UNITS + '&appid=' + API_KEY

def requestToURL(url):
    request = urllib.request.urlopen(url)
    response = request.read().decode('utf-8')
    request.close()
    return json.loads(response)

def getData():
    
    # Generating URL with prefered unit and with own API_KEY
    url = urlBuild()
    print('URL: ' + url + '\n')

    # Sending request to URL and storing it 
    jsonResponse = requestToURL(url)
    print('Response: ' + json.dumps(jsonResponse) + '\n')
    
    # Getting date from python lib
    todayDate = datetime.datetime.today()
    todayDate = todayDate.strftime('%d/%m/%y')
    timeNow = datetime.datetime.now().time()
    timeNow = timeNow.strftime('%H:%M:%S')


    # Parsing data from request
    temperature = str(jsonResponse['main']['temp']) + ' C'
    weather = jsonResponse['weather'][0]['description']
    humidity = str(jsonResponse['main']['humidity']) + '%'
    # timestamp = jsonResponse['dt']

    # Checking infos
    print('Date: ' + todayDate)
    print('Time: ' + timeNow)
    #tu print('Timestamp: %d ' % timestamp)
    print('Temperature: ' + temperature)
    print('Weather: ' + weather)
    print('Humidity: ' + humidity)

    data = todayDate + ';' + timeNow + ';' + temperature + ';' + weather + ';' + humidity

    return data

def main():
    arduinoSerial = serial.Serial('/dev/ttyACM0', 9600)

    time.sleep(1.8)

    # Checking arduino port
    print('\n')
    print(arduinoSerial.portstr)
    
    while 1:
        info = getData()
        print('Enviando informações para serial\n')
        arduinoSerial.write(str(info).encode())
        # Must change to 3600 for an hour delay
        time.sleep(60)


if __name__ == '__main__':
    main()