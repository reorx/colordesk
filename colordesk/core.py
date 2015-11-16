#!/usr/bin/env python
# coding: utf-8

import yaml

filename = 'example.yaml'

with open(filename, 'r') as f:
    text = f.read()

loaded = yaml.load_all(text)
print [i for i in loaded]
