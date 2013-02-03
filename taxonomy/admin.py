#!/usr/bin/env python
# encoding: utf-8

from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from taxonomy.models import Taxon, TaxonRank

class TaxonAdmin(MPTTModelAdmin):
    list_display = ('_name', 'breadcrumb')
    #prepopulated_fields = {'slug': ('title',)}
    mptt_level_indent = 20

admin.site.register(Taxon, TaxonAdmin)
admin.site.register(TaxonRank)