#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from taxonomy.utils import enum

SITE_POLICY = enum(FK=0, M2M=1)

class FKSitePolicy(object):
    site = models.ForeignKey(Site)

    on_site = CurrentSiteManager()

    def save(self, ref_obj=None, *args, **kwargs):
        if not self.site:
            self.site = Site.objects.get(pk=settings.SITE_ID)
        if ref_obj and self.site != ref_obj.site:
            raise ValueError(_(u"'%s' doesn't match reference '%s'" % (self.site, ref_obj.site) ))
        super(FKSitePolicy, self).save(*args, **kwargs)


class M2MSitePolicy(object):
    sites = models.ManyToManyField(Site)

    on_site = CurrentSiteManager()

    def save(self, ref_obj=None, *args, **kwargs):
        current_site = Site.objects.get(pk=settings.SITE_ID)
        if ref_obj and current_site not in ref_obj.sites.all():
            raise ValueError(_(u"'%s' not in in_sites [%s]" % (self.site, ref_obj.sites.all()) ))
        else:
            super(M2MSitePolicy, self).save(*args, **kwargs)
            self.sites.add(current_site)




def get_site_policy_model_mixin(site_policy):
    if site_policy == SITE_POLICY.M2M:
        return M2MSitePolicy
    else:
        return FKSitePolicy