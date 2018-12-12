API_KEY = 'a31d9ea1bdc6a01f8413f8da791f08e9'
URL = 'http://api.openweathermap.org/data/2.5/weather?'
CITY_NAME = 'Maringá'
CITY_ID = '6322863'
UNITS = 'metric'
timeStamp = 0.0

import urllib.request
import json
import datetime
import serial
import time
import math

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
    timeStamp = time.time()
    trash, timeStamp = math.modf(timeStamp)
    timeStamp = int(timeStamp-7180)
    timeNow = 'T' + str(timeStamp)

    # Checking infos
    print('Timestamp: %d ' % timeStamp)
    print('Temperature: ' + temperature)
    print('Weather: ' + weather)
    print('Humidity: ' + humidity)

    data = timeNow + ';' + temperature + ';' + weather + ';' + humidity

    return data

def main():
    arduinoSerial = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)
    # Checking arduino port
    print('\n')
    print(arduinoSerial.portstr)

    while 1:
        time.sleep(5)
        info = getData()
        print('Enviando informações para serial\n')
        print(info)
        arduinoSerial.write(str(info).encode())
            # Must change to 3600 for an hour delay


if __name__ == '__main__':
    main()