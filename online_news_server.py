from flask import Flask, render_template, request
from datetime import datetime, timedelta 

import asyncio
import requests
import serial
import time

app = Flask(__name__)

# Establish serial connection and flush any previous serial data
# Note: Should make port selection in browser
ser = serial.Serial('/dev/ttyUSB0', 57600)
ser.flush()

serial_lock = asyncio.Lock()

# Hardcoded URL for news server
#url = 'https://newsapi.org/v2/top-headlines?'
url = 'https://newsapi.org/v2/everything?'

# Hardcoded sort selection
# Note: Need to add this to selection on server
sort = 'popularity'

# Initial page view
# Note: Do I need two page views?
@app.route('/')
def index():
	return render_template('news.html')

# Gather form entries from news page. 
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
	# Create list of news sources
	source_set = ','.join(sources)
	
	# Calculate correct date based on number of past days requested for search
	dt = datetime.now() -timedelta(days = int(days))
	month = dt.month
	day = dt.day

	# Collect all parameters for search request
	params.update( {'from' : '2020-{}-{}'.format(month, day)} )
	params.update( {'domains' : '{}'.format(source_set)} )
	params.update( {'qInTitle' : '{}'.format(search)} )
	params.update( {'sortBy' : '{}'.format(sort)} )

	# Make request to NewsAPI
	response = requests.get(url, params=params)

	# Print params and return result of search request as json
	print(params)
	return response.json()

def display_news(news):
	for article in news['articles']:
		title = article['title'].upper()
		async with serial_lock:
			print(title)
			for letter in title:
				print(letter)
				#ser.write(letter.encode())
				time.sleep(.3)
			#ser.write(" ++ ".encode())

def main():
	news = generate_news()
	display_news(news)

if __name__ == "__main__":
	#main()
	app.run(debug=True)

