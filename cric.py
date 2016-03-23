import re
import time
import urllib2
import subprocess
from bs4 import BeautifulSoup as bs

#donwloads and parses webpage
def load_over():
	
	global soup, commentary
	soup = bs(urllib2.urlopen('http://www.cricbuzz.com/live-cricket-scores/15794/').read())	
	
	curovr=(soup.find("div", class_="cb-ovr-num"))

	if curovr:
		commentary=curovr.parent.next_sibling.get_text()
		commentary=commentary.lower()
		return True
	else:
		return False

#language processing
def chkmsg():

	if 'four' in commentary:	
		notify('4, "{0}" '.format(commentary))

	elif 'six' in commentary: 
		notify('6, "{0}"'.format(commentary))

	elif 'out' in commentary:

	#check for wicket type with regex 	 

		if re.search('\w* c\s\w*\sb\s\w*', commentary): 
			notify('caught, "{0}"'.format(commentary))
		elif re.search('\w*\sst\s\w*\sb\s\w*', commentary):
			notify('stumped, "{0}"'.format(commentary))
		elif re.search('\w*\sb\s\w*', commentary):
			notify('bowled, "{0}"'.format(commentary))
		elif re.search('\w*\srun out\s\w*', commentary):
			notify('run out, "{0}"'.format(commentary))
	return
	
#desktop notification
def notify(msg):

	subprocess.Popen(['notify-send', msg])
	return 

while True:
	if load_over():
		chkmsg()
	print("Loop")
	time.sleep(5)


