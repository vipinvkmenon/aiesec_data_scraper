import aiesec_scraper
import eplistfile


username = " "  #the myaiesec id in double quotes
password = " " #password
aiesec_scraper.aiesec_browser_init(username,password)
f = open("testfile.csv","w+")


for eps in eplistfile.eplists:
    aiesec_scraper.aiesec_browser(eps,f)
f.close()
print " !!!!!    COMPLETED !!!"

