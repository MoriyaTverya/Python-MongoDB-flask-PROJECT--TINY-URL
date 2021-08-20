from random import choices
import string

#generate short url by random string
def generate_short_url():
    short_url = 'minilink.'
    characters = string.digits + string.ascii_letters
    short_url += ''.join(choices(characters, k=3))
    return short_url
