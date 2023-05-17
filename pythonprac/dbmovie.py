from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.h5jsrip.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


db.movies.update_one({'title':'드림'},{'$set':{'rate':0}})