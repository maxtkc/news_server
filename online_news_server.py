from flask import Flask, render_template, request
from datetime import datetime, timedelta 

import requests
import serial
import time

app = Flask(__name__)

ser = serial.Serial('/dev/ttyUSB0', 57600)
ser.flush()

#url = 'https://newsapi.org/v2/top-headlines?'
url = 'https://newsapi.org/v2/everything?'

tdays = 18
sort = 'popularity'

@app.route('/')
def index():
	return render_template('news.html')

@app.route('/view', methods = ['GET', 'POST'])
def set_parameters():
	if request.method == 'POST':
		days = request.form.get('days')
		keyword = request.form.get('keyword')
		sources = request.form.getlist('sources')
		news = generate_news(keyword, sources, days)
		display_news(news)
	return render_template('view.html')

def generate_news(search, sources, days):
	params = {
		'language': 'en',
		'apiKey': 'd326d5d1b37b4d6085e89f2c747942f2'
	}
	source_set = ','.join(sources)
	
	dt = datetime.now() -timedelta(days = int(days))
	month = dt.month
	day = dt.day

	params.update( {'from' : '2020-{}-{}'.format(month, day)} )
	params.update( {'domains' : '{}'.format(source_set)} )
	params.update( {'qInTitle' : '{}'.format(search)} )
	params.update( {'sortBy' : '{}'.format(sort)} )

	response = requests.get(url, params=params)

	print(params)
	return response.json()

def display_news(news):

	for article in news['articles']:
		print(article['title'])

	for article in news['articles']:
		title = article['title'].upper()
		for letter in title:
			print(letter, end=" ")
			#ser.write(letter.encode())
			#time.sleep(.3)
		ser.write(" ++ ".encode())

def main():
	news = generate_news()
	display_news(news)

if __name__ == "__main__":
	#main()
	app.run(debug=True)

