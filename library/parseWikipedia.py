from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import re
import logging
import urllib.request, urllib.parse, urllib.error
class parseWikipedia():
	def __init__(self,language, titleWP):
		self.language = language
		self.titleWP = titleWP
	def getRedirect(self):
		redirect = Request('https://'+self.language+'.wikipedia.org/w/api.php?action=query&titles='+self.titleWP+'&redirects=yes&format=json')
		try:
			responsePWRedirect = urlopen(redirect, timeout=5)
			wikiPediaRedirect = responsePWRedirect.read()
			jsonDataPWRedirect = json.loads(wikiPediaRedirect)
			try:
				titleRedirect = jsonDataPWRedirect["query"]["redirects"][0]["to"]
				self.titleWP = titleRedirect.encode('utf8').replace(' ', '%20')
				return self.titleWP
			except:
				logging.info("redirect title couldn't be found")
				self.titleWP = self.titleWP.replace(' ', '%20')
				return self.titleWP
		except:
			logging.info("something went wrong getting the redirect title page")
			self.titleWP = self.titleWP.replace(' ', '%20')
			return self.titleWP

	def getWikipediaJSON(self):
		wpRequest = Request('https://'+self.language+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+self.titleWP)
		logging.info('https://'+self.language+'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+self.titleWP)
		#https://en.wikipedia.org/w/api.php?action=query&titles=Elodie%20Courter&redirects=yes
		try:
			responsePW = urlopen(wpRequest, timeout=5)
			wikiPedia = responsePW.read()
			jsonDataPW = json.loads(wikiPedia)
			self.json = jsonDataPW
			keys = list(self.json["query"]["pages"].keys())
			if keys[0] == "-1":
				return False
			else:
				return True
		except:
			logging.info("cannot get wikipedia 'extract' json object")
			return False
	def getFirstSentence(self):
		try:
			keys = list(self.json["query"]["pages"].keys())
			extract = self.json["query"]["pages"][keys[0]]["extract"]
			logging.info(extract)
			firstSentence = re.search(r'^.*?\w\w+\)?\.', extract).group(0).encode("utf8")
			logging.info(firstSentence)
			self.firstSentence = firstSentence
			return firstSentence
		except:
			logging.info("problem getting first sentence")
	#

	def getPageID(self):
		try:
			keys = list(self.json["query"]["pages"].keys())
			# pageid = self.json["query"]["pages"][keys[0]]["pageid"]
			# logging.info(pageid)
			# self.pageid = pageid
			# return pageid
			print(keys[0])
			return keys[0]
		except:
			logging.info("problem getting pageid")
	#
	def getWikipediaCreator(self):
		print((urllib.parse.quote(self.titleWP)))		
		# print(self.language)
		wpRequest = Request('https://'+self.language+'.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvlimit=1&rvprop=timestamp%7Cuser%7Ccomment&rvdir=newer&titles='+urllib.parse.quote(self.titleWP))
		# wpRequest = Request('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&titles=Morris_Weinfeld&rvlimit=1&rvprop=timestamp%7Cuser%7Ccomment&rvdir=newer')
		logging.info('https://'+self.language+'.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvlimit=1&rvprop=timestamp%7Cuser%7Ccomment&rvdir=newer&titles='+urllib.parse.quote(self.titleWP))
		#https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Animation&rvlimit=1&rvprop=timestamp%7Cuser%7Ccomment&rvdir=newer

		try:
			# print ('about to try to ask for it')
			responsePW = urlopen(wpRequest, timeout=5)
			# print ('asked for it')
			wikiPedia = responsePW.read()
			# print ('read it')
			print (wikiPedia 	)
			jsonDataPW = json.loads(wikiPedia)
			self.json = jsonDataPW
			print ('loaded it')
			# print(json.dumps(self.json, indent=2))
			keys = list(self.json["query"]["pages"].keys())
			print (keys)
			# print(self.json["query"]["pages"][keys[0]]["revisions"])
			# keys2 = self.json["query"]["pages"][keys1[0]]["revisions"].keys()
			# print(keys2)

			creatorPlus = self.json["query"]["pages"][keys[0]]["revisions"][0]
			creator =creatorPlus["user"].encode("utf8")
			createDate =creatorPlus["timestamp"].encode("utf8")
			# creator = json.loads(creatorPlus)
			#creator = re.search(r'user.*', revisionObject).group(0).encode("utf8")
			# u'user': u'

			# print(json.dumps(creatorPlus, indent=2))

			# print(creatorPlus.encode('utf8'))
			# self.creatorWP = creatorPlus.encode('utf8').replace(' ', '%20')
			# print("TK:"+self.creatorWP)

#			firstSentence = creator.group(0).encode("utf8")
			# print(json.dumps(self.json, indent=2))

			logging.info(creator)
			self.creator = creator
			self.createDate = createDate
			return creator, createDate
		except:
			logging.info("cannot get wikipedia 'creator' json object")
			print("uh oh, exceptions")
			return False

	# def getReferences(self):
	# 	logging.info("getting ref")

# if this module is run directly, the following lines of code will run
if __name__ == "__main__":
	lala = parseWikipedia("en", "Mako%20Idemitsu")
	title = lala.getRedirect()
	logging.info(title)
	lala.getWikipediaJSON()
	logging.info(lala.json)
	lalasentence = lala.getFirstSentence()
	logging.info(lalasentence)
