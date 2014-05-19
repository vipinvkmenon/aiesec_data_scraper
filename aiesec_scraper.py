# AIESEC Webpage EP/TN Scraper
# By Vipin VijayKumar
# Head Global Community Deevelopment
# AIESEC Kochi (2013 - 2014)
#########################################################################

import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import urllib

br = 0

def aiesec_browser_init(user,password):
    global br
    br = mechanize.Browser()  # Browser initialised
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # The site we will navigate into, handling it's session
    br.open('http://www.myaiesec.net/login.do')

    # Select the first (index zero) form
    br.select_form(nr=0)

    # User credentials
    br.form['userName'] = user.strip(' \t\n\r')
    br.form['password'] = password.strip(' \t\n\r')

    # Login
    br.submit()

def aiesec_browser(epid,f):
    global br
    # After login we request for the unique from id
    parameters = {  "category": '8' , "normalSearchTitle" : epid.strip(' \t\n\r') } #POST request parameters
    datax = urllib.urlencode(parameters) # serialize data
    uniq_form_id =  br.open("http://www.myaiesec.net/ajaxsearchform.do?operation=getEPId",datax).read() # send request
    print "EP ID is:-> ", epid, # unique form id

    # use form id to pull the required page
    rec_prof = br.open('http://www.myaiesec.net/exchange/viewep.do?operation=executeAction&epId=' + uniq_form_id).read()
    #print rec_prof

    # start extracting data from forms
    soup = BeautifulSoup(rec_prof)

    #table = soup.find("table")
    #for row in table.findAll("tr"):
        #cells = row.findAll("td")
        #print cells

    #print soup

    left_cont_box = soup.find("div",{"class" : "left-content box"})
    left_cont_box = left_cont_box.find("table")
    for rows in left_cont_box.findAll("tr")[2:]: # skipping the first and second trs name block and date block need a beeter ways
    # to handle them... ippol thalkaalam shemi    :P
        for cols in rows.findAll("td")[1:]:  # we skip titles...wastes of space   :)
            correct_string = cols.text.replace('&nbsp;',',').split()
            #f.write(" ".join(correct_string) + ',')
            f.write(" ".join(correct_string).encode('utf-8') + ',')
######  right column
    left_cont_box = soup.find("div",{"class" : "right-content box"})
    left_cont_box = left_cont_box.find("table")
    for rows in left_cont_box.findAll("tr")[1:]: # skipping the first and second trs name block and date block need a beeter ways
    # to handle them... ippol thalkaalam shemi    :P
        for cols in rows.findAll("td"):  # we skip titles...wastes of space   :)
            correct_string = cols.text.replace('&nbsp;',',').split()
            #f.write(" ".join(correct_string) + ',')
            f.write(" ".join(correct_string).encode('utf-8') + ',')
            #print " ".join(correct_string),
    f.write("\n")
    print "..............................  OK"
















