#!/usr/bin/env python
# coding: utf-8

import yaml
from .errors import ParseYAMLError


class ColorDoc(object):
    def __init__(self, title, description=None):
        self.title = title
        self.description = description
        self.patterns = []

    def add_pattern(self, p):
        self.patterns.append(p)


def parse_yaml(filedict):

    loop = 0
    for i in yaml.load_all(filedict['text']):
        loop += 1

        if loop == 1:
            if 'meta' in i:
                try:
                    meta = i['meta']
                    title = meta['title']
                    description = meta.get('description')
                except KeyError as e:
                    raise ParseYAMLError('In `meta`: %s' % e)
            else:
                title = filedict['name']
                description = None
            doc = ColorDoc(title, description)
        else:
            pattern = dict(i)

            format_pattern(pattern)

            doc.add_pattern(pattern)

    return doc


def format_pattern(pattern):
    """Format & check pattern dict"""
    colors = []

    for i in pattern['colors']:
        if isinstance(i, basestring):
            color = {
                'name': None,
                'color': i
            }
        else:
            try:
                color = {
                    'name': i['name'],
                    'color': i['color']
                }
            except KeyError as e:
                raise ParseYAMLError('In `colors`: %s' % e)
        colors.append(color)

    pattern['colors'] = colors
