import json
import requests


images = json.load(open('images_mw_es.json'))
url = """https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&format=json&iiprop=url&iiurlwidth=200&titles=File:"""

def get_thumb (image):
    resp = requests.get(url + image)
    thu = json.loads(resp.text)
    try:
        thumburl = thu.get('query')['pages'].values()[0]['imageinfo'][0]['thumburl']
        return thumburl
    except:
        print 'Error with',  image
        return


for i in images:
    i['thumburl'] = get_thumb(i['label'])

