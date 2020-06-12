import requests
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 57600)

#url = 'https://newsapi.org/v2/top-headlines?'
url = 'https://newsapi.org/v2/everything?'


params = dict(qInTitle='uk', sortBy='popularity', domains='bbc.com', language='en', **{'from':'2020-06-01'}, apiKey='d326d5d1b37b4d6085e89f2c747942f2')
#params = dict(qInTitle='bicycle', sortBy='popularity', apiKey='d326d5d1b37b4d6085e89f2c747942f2')

response = requests.get(url, params=params)

news = response.json()
print(type(news))

#description = news['articles'][2]['title'].upper()

#print(description)

ser.flush()

for article in news['articles']:
	print(article['title'])

x = 0
while True:
	for article in news['articles']:
		title = article['title'].upper()
		for letter in title:
			ser.write(letter.encode())
			time.sleep(.3)
		ser.write(" ++ ".encode())
