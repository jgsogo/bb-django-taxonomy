#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from taxonomy.settings import BASETAXONRANK_MIXIN, TAXONOMY_SITES_POLICY
from taxonomy.utils import load_class, get_basemodel_mixin

SITE_POLICY_MODEL_MIXIN = object
if TAXONOMY_SITES_POLICY:
    from django.conf import settings
    from django.contrib.sites.models import Site
    from taxonomy.utils import get_site_policy_model_mixin
    SITE_POLICY_MODEL_MIXIN = get_site_policy_model_mixin(TAXONOMY_SITES_POLICY)


class BaseTaxonRank(SITE_POLICY_MODEL_MIXIN, models.Model):
    index = models.PositiveIntegerField()

    class Meta:
        app_label = 'taxonomy'
        abstract = True

    def get_major_rank(self, *args, **kwargs):
        return BaseTaxonRank.objects.get(index=self.index-1)[0].index

    def get_minor_rank(self, *args, **kwargs):
        return BaseTaxonRank.objects.get(index=self.index+1)[0].index


if BASETAXONRANK_MIXIN:
    Mixin = get_basemodel_mixin(BASETAXONRANK_MIXIN):
    class TaxonRank(Mixin, BaseTaxonRank):
        class Meta(BaseTaxonRank.Meta):
            abstract = False

else:
    class TaxonRank(BaseTaxonRank):
        class Meta(BaseTaxonRank.Meta):
            abstract = False