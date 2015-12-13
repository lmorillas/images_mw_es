#  -*- coding: utf-8 -*-

import mwclient
import mwparserfromhell
import json

site = mwclient.Site(('https', 'commons.wikimedia.org'))

categories = [u'Princess of Asturias Awards 2015 - Supported by Wikimedia España',
u'Activities by Wikimedia España in 2015']

categories = [(u'Activities by Wikimedia España in 2015', )]



def data_image(im):
    data = {}
    metadata = ['DateTime', 'Artist', 'Copyright']
    for d in 'user timestamp url'.split():
        data[d] = im.imageinfo.get(d).strip()
    for d in [m for m in image.imageinfo.get('metadata') if m.get('name') in metadata]:
        data[d.get('name').lower()] = d.get('value').strip()
    data['label'] = im.page_title
    return data

def get_license(im):
    wikicode = mwparserfromhell.parse(im.text())
    for t in wikicode.filter_templates():
        if t.name.lower() == 'self':
            return unicode(t.params[0].value)

def parse_image(image, category):
    print image.page_title
    if image.page_title not in data_dict.keys():
        _tmpdata = data_image(image)
        _tmpdata['categories'] = [category]
        license = get_license(image)
        if license:
            _tmpdata['license'] = license
        data_dict[image.page_title] = _tmpdata
    else:
        data_dict[image.page_title]['categories'].append(category)

data_dict = {}
inspected = []
result = []

while categories:
    category = categories.pop()
    inspected.append(category[0])
    result.append(category)

    for element in site.Categories[category[0]]:
        if isinstance(element, mwclient.listing.Category):
            if element not in inspected:
                categories.append((element.page_title, category))
                print 'Categoria: ', element.page_title
        elif isinstance(element, mwclient.page.Image):
            parse_image(element, category)

# save json data
json.dump(data_dict.values(), open('images_mw_es.json', 'w'))
