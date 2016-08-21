from pymongo import MongoClient
from bson.objectid import ObjectId

class classMongodb:
	db = ''
	client = ''
	CONST_HOST = ''
	CONST_PORT = ''

	def __init__(self, hostname='127.0.0.1', port='27017'):
		self.CONST_HOST = hostname
		self.CONST_PORT = port
		self.client = MongoClient('mongodb://' + self.CONST_HOST + ':' + self.CONST_PORT)

		# database = bryanyuan2
		self.db = self.client.bryanyuan2

	def dbCleanAll(self, field):
		allChar = self.db.act.find()
		for char in allChar:
			for item in field:
				result = self.db.act.update({ "_id": char['_id'] },
		    		{ "$set" : { item : 0 } }
				)
	def dbFindTargetActObjID(self, name):
		getAct = self.db.act.find_one({'char': name})
		return getAct['_id']
	def dbFindTargetActObjCount(self, name):
		getAct = self.db.act.find_one({'char': name})
		return getAct['count']
	def dbCountRelatedActor(self):
		actors = self.db.act.find()
		count = 0
		for target in actors:
			relatedSetHash = set()
			actualAry = []

			# dealing with fuzzy name for each charactor
			for fuzzy in target['char']:
				allRelated = self.db.novel.find({'char': fuzzy})
				for i in allRelated:
					allRelatedChar = i['char']
					if (len(allRelatedChar) >= 2):
						allRelatedChar.remove(fuzzy)

						# reach related char for iterate each one
						for reachRel in allRelatedChar:
							gid = self.dbFindTargetActObjID(reachRel)
							gcount = self.dbFindTargetActObjCount(reachRel)

							# new charactor never found before
							if not gid in relatedSetHash:
								actualAry.append({
									'gid': gid,
									'count': gcount,
									'name': reachRel,
									'weight': 1
								})
								# add new charactor into set
								relatedSetHash.add(gid)

							# dup charactor found
							else:
								for updateItem in actualAry:
									if (gid == updateItem['gid']):
										updateItem['weight'] = updateItem['weight'] + 1
			self.db.act.update_one(
	    		{ '_id': target['_id'] },
	    		{ '$set' : { 'relationship' : actualAry } }
			)
			count = count + 1
			print 'no:', count, ' ', target['char'][0]
			
	def dbCountActorInteraction(self):
		allChar = self.db.novel.find()
		for char in allChar:
			# if there's only 1 char in the dailog
			if (len(char['char']) == 1):
				self.db.act.update_one(
		    		{ 'char': char['char'] },
		    		{ '$inc': { 'selfcount' : 1, 'count' : 1 } }
				)
			# more than 1 chars in the dailog
			elif (len(char['char']) >= 2):
				for fuzzy in char['char']:
					self.db.act.update_one(
			    		{ 'char': fuzzy },
			    		{ '$inc' : { 'intercount' : 1, 'count' : 1 } }
					)
			else:
				continue	
