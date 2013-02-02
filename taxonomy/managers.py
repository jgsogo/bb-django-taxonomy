#!/usr/bin/env python
# encoding: utf-8

from django.db import models

from taxonomy.settings import TAXONOMY_SITES_POLICY

BaseManagerClass = models.Manager
if TAXONOMY_SITES_POLICY:
    from django.contrib.sites.managers import CurrentSiteManager
    BaseManagerClass = CurrentSiteManager

class TaxonManager(BaseManagerClass):
    def top_taxa(self):
        """
        :return: Taxa without parent
        """
        return self.filter(parent=None)

class TaxonRankManager(BaseManagerClass):
    pass