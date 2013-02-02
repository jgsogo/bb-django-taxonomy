#!/usr/bin/env python
# encoding: utf-8

from django.db import models

from taxonomy.settings import TAXONOMY_BY_SITE

BaseManagerClass = models.Manager
if TAXONOMY_BY_SITE:
    from django.contrib.sites.managers import CurrentSiteManager
    BaseManagerClass = CurrentSiteManager

class BaseTaxonManager(BaseManagerClass):
    def top_taxa(self):
        """
        :return: Taxa without parent
        """
        return self.filter(parent=None)
