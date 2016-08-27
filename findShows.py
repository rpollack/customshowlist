import urllib2
import re
from datetime import datetime
from time import strptime, mktime
from smtplib import SMTP_SSL as SMTP
from BeautifulSoup import BeautifulSoup
from prettytable import PrettyTable

#get the HTML of the web page and transform it into a BeautifulSoup object for parsing
urltograb = "http://showlistaustin.com"
html = urllib2.urlopen(urltograb).read()
showlist = BeautifulSoup(html)

#read the list of bands to search for
bandlist = open("bandlist.txt").read().splitlines()

#initialize the lists that will hold the bands that are found and the bands that are not found
intown = []
notintown = []

#search the HTML for each band you're interested in. if found, find its venue and date and add this information to a list.
for band in bandlist:
    if band: #only search if the string isn't empty (protects against blank lines)
        playing = showlist.find("td", text=re.compile(band))
        #find the <td> tag that contains the band you're interested in.
        if playing:
            #if your band was found
            #find the venue. it's in the b tag of the next a tag.
            venue = playing.findNext('a').findNext('b').string
            #find the date. it's in the b tag of the most recent h4 tag
            date = playing.findPrevious('h4').findNext('b').string
            try:
                date_object = strptime(date, '%A, %B %d, %Y')
                #convert date string into a time_struct for sorting purposes
            except Exception, e:
                print "Error converting %s to datetime" % date
            showInfo = (date_object, playing, venue)
            intown.append(showInfo)
        else:
            notintown.append(band)
            #if the band isn't playing, add it to a list of bands that weren't found.

#only try to print/email the list of shows if there is something in it
if intown:
    intown=sorted(intown)
    #sort custom showlist by date in ascending order
    
    #emailMessage = ""
    
    x = PrettyTable(["Date", "Bands", "Venue"])

    print "=== CUSTOM SHOWLIST ==="
   
    
    for show in intown:
        '''
        For each item in show, add row to output table
        ''' 
        dt = datetime.fromtimestamp(mktime(show[0])) 
        formatted_date = dt.strftime('%A, %B %d, %Y')
        #convert time_struct to seconds since epoch, then to datetime object, and then a nice pretty English format
        bands = show[1]
        venue = show[2]
        
        x.add_row([formatted_date, bands, venue])
        #creating a table is not quite working yet. when I print it it gives me errors
        
        print formatted_date, "\t", show[1], show[2]
        
        
        #emailMessage += show


# don't want to re-notify bands i've already notified about ... or, notify on them, but put them in a separate section

#sort shows by date?
