import unittest

from alephmarc21reader import AlephMarc21Reader

class TestMethods(unittest.TestCase):

    def test_author(self):
        marc21_rd = AlephMarc21Reader('test/sample_data/000055275.marc')

        author = marc21_rd.get_author()

        self.assertEqual(len(author), 1)

        self.assertEqual(author[0].name, u'Bernoulli, Daniel,')
        self.assertEqual(author[0].lifespan, u'1700-1782')
        self.assertEqual(author[0].gnd, u'(DE-588)118656503')
        self.assertEqual(author[0].role, u'aut')
