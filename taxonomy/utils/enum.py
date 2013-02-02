#!/usr/bin/env python
# encoding: utf-8

def enum(**enums):
    # http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
    return type('Enum', (), enums)