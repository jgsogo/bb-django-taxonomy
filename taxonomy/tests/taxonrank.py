#!/usr/bin/env python
# encoding: utf-8

from django.utils import unittest
from taxonomy.models import TaxonRank
from taxonomy.exceptions import TaxonRankUpperMost, TaxonRankLowerMost

class TaxonRankTestCase(unittest.TestCase):

    def setUp(self):
        self.rank1 = TaxonRank.objects.create(rank=1)
        self.rank1dupe = TaxonRank.objects.create(rank=1)
        self.rank2 = TaxonRank.objects.create(rank=2)
        self.rank3 = TaxonRank.objects.create(rank=3)
        self.rank4 = TaxonRank.objects.create(rank=4)

    def test_major_rank(self):
        """ Ensure get_major_rank works """
        self.assertEqual(self.rank4.get_major_rank(), 3)
        self.assertEqual(self.rank3.get_major_rank(), 2)
        self.assertEqual(self.rank2.get_major_rank(), 1)
        self.assertRaises(TaxonRankUpperMost, self.rank1.get_major_rank)

    def test_minor_rank(self):
        """ Ensure get_minor_rank works """
        self.assertEqual(self.rank1.get_minor_rank(), 2)
        self.assertEqual(self.rank2.get_minor_rank(), 3)
        self.assertEqual(self.rank3.get_minor_rank(), 4)
        self.assertRaises(TaxonRankLowerMost, self.rank4.get_minor_rank)
