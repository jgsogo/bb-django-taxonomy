#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from taxonomy.settings import BASETAXONRANK_MIXIN, TAXONOMY_SITES_POLICY
from taxonomy.utils import load_class, get_basemodel_mixin, get_site_policy_model_mixin
from taxonomy.managers import TaxonRankManager
from taxonomy.exceptions import TaxonRankUpperMost, TaxonRankLowerMost

SITE_POLICY_MODEL_MIXIN = get_site_policy_model_mixin(TAXONOMY_SITES_POLICY)

class BaseTaxonRank(SITE_POLICY_MODEL_MIXIN):
    rank = models.PositiveIntegerField()

    class Meta:
        ordering = ['rank',]
        app_label = 'taxonomy'
        abstract = True

    def get_major_rank(self, *args, **kwargs):
        try:
            return self.__class__.objects.filter(rank=self.rank-1)[0].rank
        except IndexError:
            raise TaxonRankUpperMost

    def get_minor_rank(self, *args, **kwargs):
        try:
            return self.__class__.objects.filter(rank=self.rank+1)[0].rank
        except IndexError:
            raise TaxonRankLowerMost



if BASETAXONRANK_MIXIN:
    Mixin = get_basemodel_mixin(BASETAXONRANK_MIXIN, ['rank',])
    class TaxonRank(Mixin, BaseTaxonRank):
        class Meta(Mixin.Meta, BaseTaxonRank.Meta):
            abstract = False

else:
    class TaxonRank(BaseTaxonRank):
        objects = TaxonRankManager()
        class Meta(BaseTaxonRank.Meta):
            abstract = False