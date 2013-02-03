#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.template.defaultfilters import slugify
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from taxonomy.settings import BASETAXON_MIXIN, TAXONRANK_SEPARATOR, TAXONOMY_SITES_POLICY, TAXONOMY_RANKED
from taxonomy.utils import load_class, get_basemodel_mixin, get_site_policy_model_mixin
from taxonomy.models.taxonrank import TaxonRank

SITE_POLICY_MODEL_MIXIN = get_site_policy_model_mixin(TAXONOMY_SITES_POLICY)


class TT(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

class BaseTaxon(MPTTModel, SITE_POLICY_MODEL_MIXIN):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    if TAXONOMY_RANKED:
        rank = models.ForeignKey(TaxonRank)

    class Meta(SITE_POLICY_MODEL_MIXIN.Meta):
        app_label = 'taxonomy'
        abstract = True

    def __unicode__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.get_name())
        return self.get_separator().join(p_list)

    def get_name(self):
        return str(self.pk)
    _name = property(get_name)

    def _recurse_for_parents(self, obj):
        p_list = []
        if obj.parent_id:
            p = obj.parent
            p_list.append(p.get_name())
            more = self._recurse_for_parents(p)
            p_list.extend(more)
        if obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return TAXONRANK_SEPARATOR or ' :: '

    @property
    def breadcrumb(self):
        p_list = self._recurse_for_parents(self)
        return self.get_separator().join(p_list)

    def save(self, *args, **kwargs):
        p_list = self._recurse_for_parents(self)
        if self.get_name() in p_list:
            raise validators.ValidationError(_(u'You must not save a taxon in itself!'))
        super(BaseTaxon, self).save(ref_obj=self.parent, *args, **kwargs)

if BASETAXON_MIXIN:
    Mixin = get_basemodel_mixin(BASETAXON_MIXIN, ['_name','parent', 'rank'])
    class Taxon(BaseTaxon, Mixin):

        class Meta(BaseTaxon.Meta, Mixin.Meta):
            abstract = False

else:
    class Taxon(BaseTaxon):
        class Meta(BaseTaxon.Meta):
            verbose_name = 'taxon'
            verbose_name_plural = 'taxa'
            abstract = False

