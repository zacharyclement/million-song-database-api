# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import hdf5_getters as GETTERS
import beat_aligned_feats as BEAT

#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

e = create_engine('sqlite:///subset_track_metadata.db')

app = Flask(__name__)
api = Api(app)

class Get_Song_Name(Resource):
    def get(self, artist_name):
        conn = e.connect()
        query = conn.execute("select title from songs where artist_name='%s'"%artist_name)
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class Get_Song_Data(Resource):
    def get(self, song_name):
        conn = e.connect()
        query = conn.execute("select track_id from songs where title='%s'"%song_name)
        for row in query:
            song = row['track_id']
            song = str(song)
            file_str = song
            file_h5 = file_str + '.h5'
            #start = file_str[:2]
            third = file_str[2]
            fourth = file_str[3]
            fifth = file_str[4]
            #end = file_str[5:]
            path = 'data/' + str(third) + '/' + str(fourth) + '/' + str(fifth) + '/' + file_h5 

            h5 = GETTERS.open_h5_file_read(path)
            artist = GETTERS.get_artist_name(h5)
            title = GETTERS.get_title(h5)
            print('artist: ', artist, ' ', 'title: ', title)

            chroma = BEAT.get_btchromas(h5)
            timbre = BEAT.get_bttimbre(h5)
            loudness_max = BEAT.get_btloudnessmax(h5)
            chroma_loudness = BEAT.get_btchromas_loudness(h5)
            
            #print loudness_max
            #convert np array to list
            chroma = chroma.tolist()
            timbre = timbre.tolist()
            loudness_max = loudness_max.tolist()
            chroma_loudness = chroma_loudness.tolist()

            #check data type
            chroma_object = {}
            for x in range(len(chroma)):
                chroma_object[x] = dumps((chroma[x]))

            timbre_object = {}
            for x in range(len(timbre)):
                timbre_object[x] = dumps((timbre[x]))

            loudness_max_object = {}
            for x in range(len(loudness_max)):
                loudness_max_object[x] = dumps((loudness_max[x]))

            chroma_loudness_object = {}
            for x in range(len(chroma_loudness)):
                chroma_loudness_object[x] = dumps((chroma_loudness[x]))

            json_data = {}
            json_data['chroma'] = chroma_object
            json_data['timbre'] = timbre_object
            json_data['loudness-max'] = loudness_max_object
            json_data['chroma-loudness-oject'] = chroma_loudness_object
            
            return json_data
            
api.add_resource(Get_Song_Name, '/artist/<string:artist_name>')
api.add_resource(Get_Song_Data, '/song/<string:song_name>')

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)	