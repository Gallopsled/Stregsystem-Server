import cherrypy
import sqlite3
import os
import json

db_name = "stregliste.db"


class Stregliste(object):

	"""
		Example: action=register_user&params={"cardid": 1234, "username": "Ninn"}
	"""
	def handle_create_user(self, params):
		try:
			data = json.loads(params)
		except:
			return "Could not load json from %s " % params

		for i in ['cardid', 'username']:
			if not i in data.keys():
				return "Could not find %s" % i

		try:
			with sqlite3.connect(db_name) as c:
				c.execute('INSERT INTO users VALUES (?,?,0)', (data['cardid'], data['username']))
				c.commit()
			return json.dumps({'status':"Registration successful"})
		except:
			# TODO: Check why it failed?
			return json.dumps({'status':"Registration failed"})

	"""
		Example: action=resupply&params={"buyer": "Ninn", "current_stock": 0, "new_stock": 9, "stock_price": 36}
	"""
	def handle_resupply(self, params):
		try:
			data = json.loads(params)
		except:
			return "Could not load json from %s " % params

		for i in ['buyer', 'current_stock', 'new_stock', 'stock_price']:
			if not i in data.keys():
				return "Could not find %s" % i

		# TODO: Check if username exists
		try:
			with sqlite3.connect(db_name) as c:
				c.execute('INSERT INTO resupplys VALUES (?,?,?,?)', (data['buyer'], data['current_stock'], data['new_stock'], data['stock_price']))
				c.commit()
			return json.dumps({'status':"Resupply successful"})
		except:
			# TODO: Check why it failed?
			return json.dumps({'status':"Resupply failed"})


	"""
		Example: action=buy_one&params={"cardid": "1234"}
	"""
	def handle_buy_one(self, params):
		try:
			data = json.loads(params)
		except:
			return "Could not load json from %s " % params

		for i in ['cardid']:
			if not i in data.keys():
				return "Could not find %s" % i

		#try:
		with sqlite3.connect(db_name) as c:
			c.execute(' INSERT INTO purchases VALUES (?,1,(select max(rowid) from resupplys))', (data['cardid'],)) #Wired ass comma shit fuck bug wut?
			c.commit()
		return json.dumps({'status':"Buy one successful"})
		#except:
			# TODO: Check why it failed?
		#	return json.dumps({'status':"Buy one failed"})


	@cherrypy.expose
	def index(self):
		return "To do: Implement overview of shit and registration"

	@cherrypy.expose
	def api(self, action, params):
		if action == None or params == None:
			return 'U wot mate?'
		elif action == "register_user":
			return self.handle_create_user(params)
		elif action == "resupply":
			return self.handle_resupply(params)
		elif action == "buy_one":
			return self.handle_buy_one(params)
		else:
			return "We are yet to implement " + action


def setup_database():
	with sqlite3.connect(db_name) as c:
		c.execute("CREATE TABLE IF NOT EXISTS users (cardid, username UNIQUE, starting_balance)")
		c.execute("CREATE TABLE IF NOT EXISTS purchases (cardid, items, supplyid)")
		c.execute("CREATE TABLE IF NOT EXISTS resupplys (buyer, current_stock, new_stock, stock_price)")
		c.commit()

if __name__ == '__main__':
	cherrypy.engine.subscribe('start', setup_database)
	cherrypy.quickstart(Stregliste())



