from urllib.request import Request, urlopen
from urllib.error import URLError
import json
import re
import logging


class parseWikidata:
	def __init__(self,language,title,qid, useQID):
		self.language = language
		self.useQID = useQID
		self.title = title
		self.qid = qid
		self.pData = {}
	def getWikiData(self):
		if self.useQID:
			request = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&sites='+self.language+'wiki&ids='+self.qid+'&languages='+self.language+'&props=claims%7Clabels%7Csitelinks/urls&sitefilter='+self.language+'wiki&format=json')
		else:
			request = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&sites='+self.language+'wiki&titles='+self.title+'&languages='+self.language+'&props=claims%7Clabels%7Csitelinks/urls&sitefilter='+self.language+'wiki&format=json')
		logging.info('https://www.wikidata.org/w/api.php?action=wbgetentities&sites='+self.language+'wiki&titles='+self.title+'&languages='+self.language+'&props=claims%7Clabels%7Csitelinks/urls&sitefilter='+self.language+'wiki&format=json')
		try:
			response = urlopen(request, timeout=5)
			wikiData = response.read()
			jsonData = json.loads(wikiData)
			self.jsonData = jsonData
			return jsonData
		except:
		    logging.info('General error. Cannot get the wikidata json')
	def getWikipediaLink(self):
		try:
			wikipediaLink = ''
			wikipediaLink = self.jsonData["entities"][self.qid]["sitelinks"][self.language+'wiki']["url"]
			return wikipediaLink
		except:
			logging.info('Error, cannot get wikilink')

	def getQID(self):
		try:
			keys = list(self.jsonData["entities"].keys())
			entitiesFound = True
			for key in keys:
				qid = key
				self.qid = qid
				return qid
		except:
			logging.info("cannot find entities")
	def getPData(self, pID):
		try:
			pQID = (self.jsonData["entities"][self.qid]["claims"][pID][0]["mainsnak"]["datavalue"]["value"]["id"])
			logging.info(self.jsonData["entities"][self.qid]["claims"][pID][0]["mainsnak"]["datavalue"]["value"]["id"])
			if pQID:
				pRequest = Request('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+pQID+'&props=descriptions%7Clabels&languages=en&format=json')
				try:
					pResponse = urlopen(pRequest, timeout=5)
					pData = pResponse.read()
					pJsonData = json.loads(pData)
					# logging.info(pJsonData)
					# logging.info(pJsonData["entities"][x]["labels"]["en"]["value"])
					if "en" in list(pJsonData["entities"][pQID]["labels"].keys()):
		 				pValue= pJsonData["entities"][pQID]["labels"]["en"]["value"].encode("utf8")
					else:
						pValue = pJsonData["entities"][pQID]["descriptions"]["en"]["value"].encode("utf8")
					self.pData[pID] = [pQID, pValue]
					logging.info(self.pData)
					return [pID, pQID, pValue]
				except:
					logging.info('No pValue')
					self.pData[pID] = [pQID, '']
					return [pID, pQID, '']
		except:
			logging.info("no pqid")
			self.pData[pID] = ['', '']
			return [pID, '', '']
