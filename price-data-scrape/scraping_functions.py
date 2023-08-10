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
