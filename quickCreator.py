from urllib.request import Request, urlopen
from urllib.error import URLError
import os, json, csv

import re
import logging, sys
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p: ')

from library.masterSettings import *
from library.QIDfromCategories import getQidFromCategories
from library.findFromFirstSentence import findFromFirstSentence
from library.parseWikidata import parseWikidata
from library.parseWikipedia import parseWikipedia
from library.handleReferences import References

print(debug)
if debug:
	outlevel = logging.DEBUG
else:

	outlevel = logging.CRITICAL

logging.getLogger().setLevel(outlevel)

inputFileName = inputFileNameQuickSheets


logging.debug('A debug message!')
#make a module for this whole section where you are creating directories and output files
if not os.path.exists(inputFileName+" Outputs"):
	os.makedirs(inputFileName+" Outputs")

#output file for Creator
outputwpCreator = open(inputFileName+' Outputs/wpCreator.csv', 'w')
csvWriterwpCreator = csv.writer(outputwpCreator)
csvWriterwpCreator.writerow(rowCreator)


#open the input file as a csv file
with open(inputFileName+'.csv','rU') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		qid = ''
		info = list(row)
		print (info)
		if firstline:
			if any(s in info[0].lower() for s in ["item", "qid"]):
				qidDocument = True
			else:
				qidDocument = False
			   #skip first line
			print (qidDocument)
			firstline = False
			continue
		# langTitle = info[0]
		try:
			if qidDocument:
				language = "en"
				info[0] = str(info[0]).replace('http://www.wikidata.org/entity/','')
				info[0] = str(info[0]).replace('wd:','')
				qid = info[0]
				print (qid)
			else:
				language = info[0] #get the language
		except:
			logging.info("no lang found")
		# titleOriginal = langTitle.split(':')[1]
		

		# THIS IS CUSTOMIZED FOR THE FORMAT OF all_enwiki_bios_from_wikidata.csv
		# TITLEWP IS THE FIFTH VALUE, SO ARRAY ITEM 4
		language = "en"
		qid = info[1] #get the title

		try:
			titleOriginal = info[4] #get the title
			title = titleOriginal.replace(' ', '+') #format the title for wikidata api query
			# print (title)
			# logging.info(language)
			# logging.critical("##########################################")
			# logging.critical(titleOriginal)
			titleWP=titleOriginal.replace(' ', '_') #format the title for wikipedia api query
			# print (titleWP)
			logging.info(titleWP)
		except:
			logging.info("title couldn't be read from input file")
		# WD = parseWikidata(language,title,qid,qidDocument) #call the wikidata parsing class
		# jsonData = WD.getWikiData() #get the wikidata json object
		# WPlink = ''
		# if jsonData:
		# 	WPlink = WD.getWikipediaLink()
		# 	# print WPlink
		WP = parseWikipedia(language,titleWP) #call the wikipedia parsing class
		# if jsonData and qidDocument==False:
		# 	qid = WD.getQID() #get the qid for the object
		# if qid:
		# 	if str(qid) == "-1": #if the qid returns -1 check if it has a redirect
		# 		titleOriginal = WP.getRedirect()
		# 		if titleOriginal: #if there is a redirect then update the title formats, the wikidata json object and qid
		# 			titleOriginal = titleOriginal.replace('%20',' ')
		# 			titleWP = titleOriginal.replace(' ', '%20')
		# 			title =  titleOriginal.replace(' ', '+')
		# 			jsonData = WD.getWikiData()
		# 			qid = WD.getQID()
		# hasWP = False
		# hasWP = WP.getWikipediaJSON() #get wikipedia json object
		# print("HAS WP ==================== "+str(hasWP))

		wpCreatorPlus = False
		try:
			wpCreatorPlus = WP.getWikipediaCreator() #get wikipedia json object
			print (wpCreatorPlus)
			wpCreator = wpCreatorPlus[0].decode('UTF-8')
			wpCreateDate = wpCreatorPlus[1].decode('UTF-8')
			pageid = WP.getPageID()
		except:
			logging.info("creator could not be found in query")
			wpCreator=''
			wpCreateDate=''
			pageid=''
		print("The Creator is ==================== "+ str(wpCreator) + str(wpCreateDate))
		csvWriterwpCreator.writerow([qid, wpCreator, wpCreateDate, pageid])


# 
		#here we are resetting the following values
		keys = []
		p1 = ''
		p2 = ''
		language = ''
		titleOriginal = ''
		p1Value = ''
		p2Value = ''
		firstSentence = ''
		jsonData = ''
