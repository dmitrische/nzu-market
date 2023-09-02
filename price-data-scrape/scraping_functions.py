import pandas as pd
import datetime as datetime, timedelta
import requests
from bs4 import BeautifulSoup as bs

def strings2dates(datestrings):
	
	"""
	Function taking a list of strings and returning a list of date objects.
	
	Inputs:
	------
	
	datestrings - a list of strings specifying the date in one of three 
				  expected formats:
                 
                    i) "Today %I:%M%p" for stories published today,
                   ii) Just the weekday in "%A" format, e.g. "Tuesday", 
                       for stories published in the last week.
                  iii) Full date in "%d %b %y" format for older stories.
    """
	
	# Prepare dictionary mapping last 7 weekdays to dates    
	today = datetime.today().date()
	date_map = {'Today':today}
	for i in range(1,7):
		date = today + timedelta(days=-i)
		weekday = date.strftime("%A")
		date_map[weekday] = date
	
	# Loop over supplied datestrings and generate date objects
	dates = []
	for string in datestrings:
		words = string.split()
		if words[0] in date_map:
			date = date_map[words[0]]
		else:
			date = datetime.strptime(string.strip(),"%d %b %y").date()		
		dates.append(date)

	return dates


def parse_headline(headline, print_exceptions = False):
    
	"""
	Function taking a string and returning a real-valued price or None.
    
    INPUTS:
    ------

    headline: a string with headline text
    
    OUTPUTS:
    -------
    
    price: a real-valued price extracted from headline
    """
	
	words = headline.split()
	price = None

	if('MARKET LATEST' in headline):
		# This condition catches all but one relevant story since 22 Feb 2016.
		# Note the mistyped price in headline for 28 Jun 2017, which should be blacklisted.

		# Price is quoted as last word in all but 3 headlines
		pricestring = words[-1].strip('$.')
		try:
			price = float(pricestring)
		except ValueError:
			if(print_exceptions):
				print("EXCEPTION1: '{}' is not a float!".format(pricestring))
	
	if( (price is None) and (headline.count('$') == 1) ):
		# Look for words starting with $ in 3 special cases
		
		pricestrings = [word.strip('$.') for word in words if word.startswith('$')]
		
		if(len(pricestrings) == 1):
			try:
				price = float(pricestrings[0])
			except ValueError:
				if(print_exceptions):
					print("EXCEPTION2: '{}' is not a float!".format(pricestrings[0]))

	# Could tack on more if blocks to catch more special cases
	
	return price


def parse_summary(summary, print_exceptions = False):
	
	"""
	Function taking a string and returning a real-valued price or None.	
	
    INPUTS:
    ------

    summary: a string with summary text
    
    print_exceptions: a boolean switch for all print statements
    
    OUTPUTS:
    -------
    
    price: a real-valued price extracted from headline

	"""
	
	words = summary.split()
	price = None
	
	pricestrings = []
	for i in range(1,len(words)):
		word = words[i]
		if(word.startswith('$')):
			pricestrings.append(word.strip('$.,').strip('s').removeprefix('NZ'))
		elif(word.startswith('NZD') and len(word) > 3):
			pricestrings.append(word.strip('.,').removeprefix('NZD'))
		elif(word.replace(".", "").replace(",", "").isnumeric() and words[i-1] == 'NZD'):
			pricestrings.append(word.strip('.,'))
		elif(word.startswith('($')):
			pricestrings.append(word.strip('()').strip('$s').removeprefix('NZ'))
		else:
			pass
	
	if(len(pricestrings) > 0):
		try:
			#print(pricestrings[0])
			price_value = float(pricestrings[0])
			# Shound not be below $2
			if(price_value > 1.0):
				price = price_value                
		except ValueError:
			if(print_exceptions):
				print("EXCEPTION3: '{}' is not a float!".format(pricestrings[0]))
	
	return price

def update_data(filename):

	"""
	Function updating an existing file with time-series data on NZU price.
	
	INPUTS:
	------
	
	filename: a string specifying the file name
	
	OUTPUTS:
	-------
	
	outcome: a string summarising the outcome
	"""
	
	# First load the file into a dataframe
	df0 = pd.read_csv(filename, index_col='date', parse_dates=[0])
	
	# Scrape the Jarden NZ Market Report from Carbon News website
	url="https://www.carbonnews.co.nz/"
	page = requests.get(url+"tag.asp?tag=Jarden+NZ+Market+Report")
	soup = bs(page.content, "html.parser")
	
	# Find all the h1, h2, and h3 headlines in the soup
	helements = soup.find_all(["h1","h2","h3"], class_="Headline")
	
	# Find all the accompanying summaries 
	pelements = soup.find_all("p", class_=None ) # h1 headline
	pelements+= soup.find_all("p", class_=["StoryIntro","StoryIntro_small"]) # h2 and h3 headlines
	
	# Extract headlines, datestrings, and hyperlinks
	headlines = []; datestrings = []; hrefs = []
	for i in range(len(helements)):
		body = helements[i].find("a")
		headlines.append(body.text.strip())
		hrefs.append(body.get("href"))
		# The date string is the first text before the ' - ' in the summary.
		datestrings.append(pelements[i].text.strip().split(' - ')[0])
	
	# Convert datestrings to date objects
	dates = strings2dates(datestrings)
	
	# Extract price values from headlines
	prices = [parse_headline(headlines[i]) for i in range(len(headlines))]
	
	# Generate urls for source stories
	urls = [url+hrefs[i] for i in range(len(hrefs))]
	
	# Create dataframe for stories reporting on NZU price updates
	date0 = df0.index[-1].date()
	data = {'date':[], 'price':[], 'url':[]}
	icount = 0
	for i in range(1,1+len(dates)):
		if(dates[-i] > date0 and prices[-i] is not None):
			data['date'].append(dates[-i])
			data['price'].append(prices[-i])
			data['url'].append(url+hrefs[-i])
			icount += 1
	df1 = pd.DataFrame(data)
	
	# append data frame to CSV file
	df1.to_csv(filename, mode='a', index=False, header=False)
	
	outcome = 'Appended '+str(icount)+' rows.'
	
	return outcome
