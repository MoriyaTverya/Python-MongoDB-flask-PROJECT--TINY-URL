from pymongo import MongoClient
from shortUrl import generate_short_url

# connect to DB 
client = MongoClient("mongodb+srv://Moriya:minilink@minilink.j95fj.mongodb.net/Minilink?retryWrites=true&w=majority")
db = client.ShortUrls


#Setting requried fonctions: 
# is_longurl_exists(long_url):  check if long url is exists
# is_shorturl_exists(short_url):   check if long url is exists
# insert_url_to_DB(short_url, long_url):   insert short and original url to database
# get_short_url(long_url):   get short url by long url given
# get_long_url(short_url):   get long url by short url
# get url data():   get database of url-shortener


def is_longurl_exists(long_url):
    return db.urls.count_documents({ 'long_url': long_url}, limit = 1)

def is_shorturl_exists(short_url):
    return db.urls.count_documents({'short_url': short_url}, limit = 1)

def insert_url_to_DB(short_url, long_url):
    link = {'long_url' : long_url , 'short_url' : short_url}
    db.urls.insert_one(link)

#get short url for long url
#return short url from db if long url exist
#else generate new short url, insert to db short-url and long-url, return short url.

def get_short_url(long_url):
    #if long url exists, return its short url
    if is_longurl_exists(long_url):
        return db.urls.find_one({ 'long_url': long_url }, {"short_url": 1, '_id': 0})["short_url"]
    
    #else generate new short url
    short_url = generate_short_url()
    
    #couse short url based on random string, there may be a collision (rarely happens) 
    #if there is collision- (shorturl already exist for another long url) generate new short url until there is no collision.
    if is_shorturl_exists(short_url):
        generate_short_url()

    #add long url and short url to the data base
    insert_url_to_DB(short_url, long_url)
     
    #return short url
    return short_url

#get long url by short url
def get_long_url(short_url):
    return db.urls.find_one({ 'short_url': short_url}, {"long_url": 1, '_id': 0})["long_url"]

#get all url data - short & long urls for display and reuse them in links pase
def get_url_data():
    corsur = db.urls
    return corsur.find()