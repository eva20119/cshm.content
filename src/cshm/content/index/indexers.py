#!/usr/bin/python
# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from cshm.content.interfaces import ICourse

@indexer(ICourse)
def index_course(obj):
    return obj.title

