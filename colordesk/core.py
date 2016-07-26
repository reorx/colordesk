#!/usr/bin/env python
# coding: utf-8

import yaml
import mistune
from .errors import ParseYAMLError


class ColorDesk(object):
    def __init__(self, title, description=None):
        self.title = title
        self.description = description
        self.description_html = mistune.markdown(description)
        self.groups = []

    def add_group(self, g):
        self.groups.append(g)


def parse_desk_yaml(filedict):

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
            desk = ColorDesk(title, description)
        else:
            group = dict(i)

            format_group(group)

            desk.add_group(group)

    return desk


def format_color(s):
    if s.startswith('#'):
        return s
    return '#' + s


def format_group(group):
    """Format & check group dict"""
    colors = []

    for i in group['colors']:
        if isinstance(i, basestring):
            color = {
                'name': None,
                'color': format_color(i)
            }
        else:
            try:
                color = {
                    'name': i['name'],
                    'color': format_color(i['color'])
                }
            except KeyError as e:
                raise ParseYAMLError('In `colors`: %s' % e)
        colors.append(color)

    group['colors'] = colors
