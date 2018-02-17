# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

e = create_engine('sqlite:///subset_track_metadata.db')

app = Flask(__name__)
api = Api(app)

class Get_Song(Resource):
    def get(self, artist_name):
        conn = e.connect()
        query = conn.execute("select title from songs where artist_name='%s'"%artist_name)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
 
api.add_resource(Get_Song, '/song/<string:artist_name>')

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)	