from googleapiclient.discovery import build
import pprint
import urllib
import re

search_engine_id = '014542702800098573769:nqgplex75-w'
API_key = ' AIzaSyD8h6vVComsR7MUxPJVYB8XQGvibf_hweQ '


def cleanhtml(raw_html):
  cleanr =re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', raw_html)
  return cleantext

def main():
	query = raw_input ('Mention The Topic Of Your Choice :  ')
	list_link = []
	service = build("customsearch", "v1",developerKey=API_key)
	res = service.cse().list(q=query + ' Questions ',cx=search_engine_id).execute()
	for each in res['items']:
		list_link.append(each['link'])
	questions = []
	for link in list_link:
		files = urllib.urlopen(link)
		for lines in files:
			if '?' in lines and '<a' not in lines and '<script' not in lines:
			   if 'label' in lines or 'div' in lines or '<p' in lines :
				lines = cleanhtml(lines)
			    	lines = lines.strip()
				lines = re.sub('.-','?',lines)
			    	index = lines.find("?")
			    	if '?' in lines[:index]:
					index2 = lines[:index].find('?')
				    	questions.append(lines[:index2+1])
					lines = lines[index2+1:]
					index = index - index2
					while '.' in lines:					
						indexstop = lines.find('.')
						if indexstop < index:
							lines = lines[indexstop + 1:]
							index = index - indexstop
						else:
							lines = lines[:index+1]
				if lines[:index+1] != '' and len(lines[:index+1]) < 80 :
					if 'which of the following' not in lines[:index+1].lower() and 'output of the program' not in lines[:index+1].lower(): 					
						 questions.append(lines[:index+1])		
		files.close()
	output = open('question_bank.txt', 'w+')
	for question in questions:
		output.write(question+'\n')
	print "Questions saved to question_bank.txt"
	output.close()
main()

