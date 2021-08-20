from pymongo import MongoClient
import validators
from flask import Flask, render_template, request, flash, redirect, url_for
from urlDB import *

app = Flask(__name__)
#Set secret key in Flask In order to use session 
app.config['SECRET_KEY'] = 'moriya'


#render homepage contains an input box, displays a short link for the original link
#get url input from the user, check integrity and return appropriate response.
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        long_url = request.form['url']
        if long_url and validators.url(long_url) :
            short_url = get_short_url(long_url)
            return render_template('index.html', short_url=short_url)
            
        flash('Valid URL is required!')
        return render_template('index.html')
        
    return render_template('index.html')


#redirect to original-url by short_url
@app.route('/<short_url>')
def url_redirect(short_url):

    #check if short url is valid - exist in url database.
    if is_shorturl_exists(short_url):
        long_url = get_long_url(short_url)
        return redirect(long_url)

    # else pop massage to the user
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))


#view (and reuse) all the links in the url database
@app.route('/links')
def stats():
    urls = get_url_data()
    return render_template('links.html', urls=urls)

#return information page about Minilink - url shortener
@app.route('/about')
def about():
    return render_template('about.html')

# run app
if __name__ == "__main__":
    app.run()

