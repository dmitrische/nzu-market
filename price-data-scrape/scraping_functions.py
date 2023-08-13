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
                  iii) Full date in "%d %b %Y" format for older stories.
    """

    from datetime import datetime
    from datetime import timedelta
    
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
	
	
	"""
	
	words = summary.split()
	price = None
	
	pricestrings = [ word.strip('$.').removeprefix('NZD').removeprefix('NZ') 
					 for word in words if 
					 (word.startswith('$') or (word.startswith('NZD') and len(word) > 3)) ]

	if(len(pricestrings) > 0):
		try:
			#print(pricestrings[0])
			price = float(pricestrings[0])
		except ValueError:
			if(print_exceptions):
				print("EXCEPTION3: '{}' is not a float!".format(pricestrings[0]))
	
	return price
