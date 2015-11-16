#!/usr/bin/env python
# coding: utf-8

import yaml


def parse_patterns_yaml(filename):
    with open(filename, 'r') as f:
        text = f.read()

    patterns = list(yaml.load_all(text))
    return patterns
