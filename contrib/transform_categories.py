#!/usr/bin/python
"""
transforms the categories.txt to a yaml file
"""

import yaml

BASE_PATH = 'xplane.org-categories'
EXT = {'text': '.txt', 'yaml': '.yaml'}

if __name__ == '__main__':
    documents = yaml.load(open(BASE_PATH + EXT['text']).read())
    yaml.dump({'X-Plane.org Categories':documents}, open(BASE_PATH + EXT['yaml'], 'w'), default_flow_style=False)

