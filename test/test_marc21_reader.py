import unittest

from Marc21_reader import marc21_reader

class TestStringMethods(unittest.TestCase):

    def test_author(self):
        marc21 = marc21_reader.get_marc21('sample_data/000055275.marc')
        records = marc21_reader.get_records(marc21)

        author = marc21_reader.get_author(records)

        self.assertEqual(len(author), 1)

        self.assertEqual(author[0]['name'], unicode('Bernoulli, Daniel,'))
        self.assertEqual(author[0]['date'], unicode('1700-1782'))
        self.assertEqual(author[0]['GND'], unicode('(DE-588)118656503'))
