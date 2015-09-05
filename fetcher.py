import urllib
import json
import os
import sys

from lxml import etree as ET
from wand.image import Image

data = urllib.urlopen('https://api.github.com/emojis').read()
emo_json = json.loads(data)

root = 'GithubEmoji.AdiumEmoticonSet'

if not os.path.exists(root):
    os.mkdir(root)

if not os.path.isdir(root):
    print "{0} is not a directory...".format(root)
    sys.exit(1)

#if not os.path.isfile(root + img):
plist = ET.Element('plist', {'version': '1.0'})
d = ET.SubElement(plist, 'dict')
ET.SubElement(d, 'key').text = 'AdiumSetVersion'
ET.SubElement(d, 'real').text = '1.0'
ET.SubElement(d, 'key').text = 'Emoticons'
emoticons = ET.SubElement(d, 'dict')

def AddElement(details, filename):
    ET.SubElement(emoticons, 'key').text = filename
    emoji = ET.SubElement(emoticons, 'dict')
    ET.SubElement(emoji, 'key').text = 'Name'
    ET.SubElement(emoji, 'string').text = details['name']
    ET.SubElement(emoji, 'key').text = 'Equivalents'
    sub = ET.SubElement(emoji, 'array')
    for code in details['codes']:
        ET.SubElement(sub, 'string').text = ':{0}:'.format(code)

emojis = {}
for key in emo_json:
    img_url = emo_json[key]
    filename = os.path.basename(img_url)
    if '?' in filename:
        filename = filename.split('?')[0]
    if filename in emojis:
        emojis[filename]['codes'].append(key)
    else:
        emojis[filename] = {
            'name': key,
            'url': img_url,
            'codes': [key]
        }

for filename in emojis:
    emoji = emojis[filename]
    img_path = '{0}/{1}'.format(root, filename)
    if not os.path.isfile(img_path):
        stream = urllib.urlopen(emoji['url'])
        try:
            with Image(file=stream) as img:
                img.resize(18, 18)
                img.save(filename=img_path)
        except Exception as e:
            print e#!/usr/bin/env python
        finally:
            stream.close()

    AddElement(emoji, filename)

with open("{0}/Emoticons.plist".format(root), 'w') as fp:
    fp.write(ET.tostring(plist, encoding="UTF-8", xml_declaration=True, pretty_print=True, doctype='<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'))
