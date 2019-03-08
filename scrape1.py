# import libraries
import urllib2
from bs4 import BeautifulSoup
quote_page = "https://ndawn.ndsu.nodak.edu/get-table.html?station=33&variable=wdmxt&variable=wdmnt&variable=wdavt&variable=wdbst&variable=wdtst&variable=wdws&variable=wdmxws&variable=wdsr&variable=wdtpet&variable=wdapet&variable=wdr&variable=wddp&variable=wdwc&ttype=weekly&quick_pick=&begin_date=2003-04-01&count=36"
page = urllib2.urlopen(quote_page)
mySoupInstance = BeautifulSoup(page, 'html.parser')