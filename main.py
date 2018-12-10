from config import *
# from utils import *

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

def main():
    # arduinoSerial = serial.Serial('/dev/ttyACM0', baudrate=9600)

    print('\nGenerating URL... ')
    url = urlBuild()
    print('URL: ' + url + '\n')

    print('Sending request to URL... \n')
    jsonResponse = requestToURL(url)
    print('Response: ' + json.dumps(jsonResponse) + '\n')

    todayDate = datetime.datetime.today()
    todayDate = todayDate.strftime('%d/%m/%y')
    
    now = datetime.datetime.now().time()
    now = now.strftime('%H:%M:%S')
    temp = str(jsonResponse['main']['temp']) + ' C'
    weather = jsonResponse['weather'][0]['description']
    humi = str(jsonResponse['main']['humidity']) + '%'

    print('Date: ' + todayDate)
    print('Time: ' + now)
    print('Temperature: ' + temp)
    print('Weather: ' + weather)
    print('Humidity: ' + humi)

    print('\n')

    # print(arduinoSerial.portstr)
    print('Enviando para serial\n')

    # arduinoSerial.write(str(now).encode())
    time.sleep(60)

if __name__ == '__main__':
    main()