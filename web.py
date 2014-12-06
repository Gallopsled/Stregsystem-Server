import cherrypy
import sqlite3
import os
import json

db_name = "stregliste.db"


class Stregliste(object):
	@cherrypy.expose
	def index(self):
		return "To do: Implement overview of shit and registration"

	@cherrypy.expose
	def api(self, action, params):
		if action == None or params == None:
			return 'U wot mate?'
		elif action == "register_user":
			try:
				data = json.loads(params)
			except:
				return params
			try:
				data['cardid']
			except:
				return "Cardid is not set"

			try:
				data['username']
			except:
				return "Username is not set"
			try:
				with sqlite3.connect(db_name) as c:
					c.execute('INSERT INTO users VALUES (?,?)', (data['cardid'], data['username']))
					c.commit()
				return json.dumps({'status':"Registration successful"})
			except:
				# TODO: Check why it failed?
				return json.dumps({'status':"Registration failed"})

		return "We are yet to implement " + action



def setup_database():
	with sqlite3.connect(db_name) as c:
		c.execute("CREATE TABLE IF NOT EXISTS users (cardid, username UNIQUE)")
		c.execute("CREATE TABLE IF NOT EXISTS purchases (cardid, value)")
		c.execute("CREATE TABLE IF NOT EXISTS resupplys (buyer, current_stock, new_stock, stock_price)")
		c.commit()

if __name__ == '__main__':
	cherrypy.engine.subscribe('start', setup_database)
	cherrypy.quickstart(Stregliste())



