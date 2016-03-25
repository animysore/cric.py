import re, os, sys, time, urllib2
from gi.repository import Notify
from bs4 import BeautifulSoup as bs

#find path of script
pathname = os.path.dirname(sys.argv[0])
loc = os.path.abspath(pathname)      

#prevovr variable to prevent multiple notifications for same over. Initially None.
prevovr = None

#donwloads and parses webpage
def load_over():
	global soup, commentary, prevovr
	soup = bs(urllib2.urlopen('http://cricbuzz.com/live-cricket-scores/15788/').read())	
	curovr=(soup.find("div", class_="cb-ovr-num"))
	if curovr:
		if curovr!=prevovr:
			commentary=curovr.parent.next_sibling.get_text()
			prevovr=curovr
			return True
		else:
			return False
	else:
		return False
#language processing
def chkmsg():
	lower=commentary.lower()
	if 'four' in lower:	
		notify('Four!', '{0}'.format(commentary), '{0}/res/f.png'.format(loc))
	elif 'six' in lower: 
		notify('Six!', '{0}'.format(commentary), '{0}/res/s.png'.format(loc))
	elif 'out' in lower:
	#check for wicket type with regex 	 

		if re.search('\w*\sc\s\w*\sb\s\w*', commentary): 
			notify('Caught!', '{0}'.format(commentary), '{0}/res/o.jpg'.format(loc))
		elif re.search('\w*\sst\s\w*\sb\s\w*', commentary):
			notify('Stumped!', '{0}'.format(commentary), '{0}/res/o.jpg'.format(loc))
		elif re.search('\w*\sb\s\w*', commentary):
			notify('Bowled!', '{0}'.format(commentary), '{0}/res/o.jpg'.format(loc))
		elif re.search('\w*\srun out\s\w*', commentary):
			notify('Run Out!', '{0}'.format(commentary), '{0}/res/o.jpg'.format(loc))
	return
#desktop notification
def notify(title, message, icon):
    Notify.init("Cric")
    notice = Notify.Notification.new(title, message, icon)
    notice.show()
    return
#control loop
while True:
	if load_over():
		chkmsg()
	print("Loop")
	time.sleep(10)