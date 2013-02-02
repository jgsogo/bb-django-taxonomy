#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings

BASETAXON_MIXIN = getattr(settings, 'TAXONOMY_BASETAXON_MIXIN', None)
BASETAXONRANK_MIXIN = getattr(settings, 'TAXONOMY_BASETAXONRANK_MIXIN', None)
TAXONRANK_SEPARATOR = getattr(settings, 'TAXONOMY_TAXONRANK_SEPARATOR', None)
TAXONOMY_SITES_POLICY = getattr(settings, 'TAXONOMY_SITES_POLICY', True) # Use choices 'FK' (default) or 'M2M'