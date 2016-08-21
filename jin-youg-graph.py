#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re, json, csv, md5
from classMongodb import classMongodb

reload(sys)
sys.setdefaultencoding('utf-8')

class classAnalysis:
	# structure
	novelData = ''
	character = {};

	# const
	SPEAKCONST = '：「'
	RESOURCE_PATH = 'resource/'
	OUTPUT_PATH = 'output/'
	NOVEL_FILENAME = RESOURCE_PATH + 'text/test.txt'
	CHAR_FILENAME = RESOURCE_PATH + 'char/char.csv'

	def __init__(self, fileName):

		#db = classMongodb('127.0.0.1', '27017')

		# dbCleanAll
		#db.dbCleanAll(['count', 'selfcount', 'intercount'])

		# dbCountActorInteraction
		#db.dbCountActorInteraction()

		# dbCountRelatedActor
		
		# this
		#db.dbCountRelatedActor()

		###
		### init get novel text and extract chars
		###
		
		self.getCharacter(self.CHAR_FILENAME)
		self.readNovel(self.NOVEL_FILENAME)

		flatten = ''
		tLen = float(len(self.novelData))
		for sentance in xrange(0, len(self.novelData)):
			row = {}
			char = []

			text = self.novelData[sentance].decode('UTF-8').encode()
			getQut = self.getQuote(text)
			
			getType = self.getType(text)
			getChar = self.getChar(text)
			getCharLen = len(getChar)
			speakingIndex = self.getSpeakingIndex(text)

			row['text'] = text
			row['nchar'] = getCharLen
			row['pos'] = round(sentance/tLen, 6)
			row['source'] = '天龍八部'
			row['char'] = getChar
			#row['type'] = getType
			#row['index'] = speakingIndex

			flatten += json.dumps(row, ensure_ascii=False, indent=2)
			flatten += '\n'
		self.outputJson("final.json", flatten)
		
	def getCharacter(self, fileName):
		flatten = ''
		counter = 0
		f = open(fileName, 'r')
		for char in csv.reader(f):
		    actObj = {}
		    self.character[counter] = char
		    actObj['char'] = char
		    counter = counter + 1
		    flatten += json.dumps(actObj, ensure_ascii=False, indent=2)
		    flatten += '\n'
		f.close()

		self.outputJson("charjson.json", flatten)

	def readNovel(self, fileName = 'test.txt'):
		self.novelData = open(fileName).read().split("\n")
		# remove empty element
		self.novelData = filter(None, self.novelData)
	def getType(self, text):
		type= 'conv'
		if (text.find(self.SPEAKCONST) == -1):
			type = 'stat'
		return type
	def getChar(self, text):
		charList = []
		# get all chars
		for chars in self.character:
			naming = self.character[chars]
			knownNaming = naming[0].strip()
			for char in naming:
				# fill match
				index = text.find(char.strip())

				# partical match
				particalCo = 0
				isPartical = False
				currChar = char.decode()
				for each in list(currChar):
					if (currChar.find(char.strip())):
						particalCo = particalCo + 1

				if (particalCo == len(list(char.decode()))):
					isPartical = True

				if (index != -1 or isPartical == True):
					charList.append(knownNaming)
		return charList
	def outputJson(self, fileName, obj):
		target = open(fileName, 'w')
		target.write(obj);
		target.close()	
	#
	# deprecated method
	#
	def getQuote(self, text):
		matches=re.findall(r'\：\「(.+?)\」',text)
		return ",".join(matches)
	def getSpeakingIndex(self, text):
		# get: sepaking index
		return self.__findAll(text, self.SPEAKCONST)
	def __findAll(self, str, sub):
	    return [i for i in range(len(str)) if str.startswith(sub, i)]
test = classAnalysis("test.txt")