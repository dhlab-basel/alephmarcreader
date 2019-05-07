import unittest

from alephmarcreader import AlephMarcXMLReader

class TestMethods(unittest.TestCase):
    def test_author(self):
        marcxml_rd = AlephMarcXMLReader('alephmarcreader/tests/sample_data/000055275.xml')

        author = marcxml_rd.get_author()

        self.assertEqual(len(author), 1)

        self.assertEqual(author[0].name, u'Bernoulli, Daniel')
        self.assertEqual(author[0].lifespan, u'1700-1782')
        self.assertEqual(author[0].gnd, u'(DE-588)118656503')
        self.assertEqual(author[0].role, u'aut')

    def test_recipient(self):
        marcxml_rd = AlephMarcXMLReader('alephmarcreader/tests/sample_data/000055275.xml')

        recipient = marcxml_rd.get_recipient()

        self.assertEqual(len(recipient), 1)

        self.assertEqual(recipient[0].name, u'Scheuchzer, Johann')
        self.assertEqual(recipient[0].lifespan, u'1684-1738')
        self.assertEqual(recipient[0].gnd, u'(DE-588)120379260')
        self.assertEqual(recipient[0].role, u'rcp')

    def test_mentioned_person(self):
        marcxml_rd = AlephMarcXMLReader('alephmarcreader/tests/sample_data/000055275.xml')

        mentioned = marcxml_rd.get_mentioned_person()

        self.assertEqual(len(mentioned), 6)

        self.assertEqual(mentioned[0].name, u'Bernoulli, Johann')
        self.assertEqual(mentioned[0].lifespan, u'1667-1748')
        self.assertEqual(mentioned[0].gnd, u'(DE-588)118509969')
        self.assertEqual(mentioned[0].role, False)

    def test_date(self):
        marcxml_rd = AlephMarcXMLReader('alephmarcreader/tests/sample_data/000055275.xml')

        date = marcxml_rd.get_date()

        self.assertEqual(len(date), 1)

        self.assertEqual(date[0], u'1734.03.12')

    def test_creation_place(self):
        marcxml_rd = AlephMarcXMLReader('alephmarcreader/tests/sample_data/000055275.xml')

        cp = marcxml_rd.get_creation_place()

        self.assertEqual(len(cp), 1)

        self.assertEqual(cp[0].name, u'Basel')
        self.assertEqual(cp[0].gnd, u'(DE-588)4004617-5')

    def test_get_shelfmark(self):
        marcxml_rd = AlephMarcXMLReader('alephmarcreader/tests/sample_data/000055275.xml')

        sm = marcxml_rd.get_shelfmark()

        self.assertEqual(len(sm), 1)

        self.assertEqual(sm[0].institution, u'ZB Z\xfcrich')
        self.assertEqual(sm[0].identifier, u'Ms H 340, pp. 569-572')

    def test_get_footnote(self):
        marcxml_rd = AlephMarcXMLReader('alephmarcreader/tests/sample_data/000055275.xml')

        footnote = marcxml_rd.get_footnote()

        self.assertEqual(len(footnote), 1)

        self.assertEqual(footnote[0], u'Die Briefhandschrift findet sich in einem Z\xfcricher Briefband mit der Aufschrift "Epistolae Helvetorum ad J. J. Scheuchzer". Johann Jakob Scheuchzer starb jedoch am 23.6.1733. Daniel Bernoulli hatte von dessen Tod sp\xe4testens im August 1733 auf der R\xfcckreise von St. Petersburg erfahren (s. Brief von Johann II Bernoulli an Leonhard Euler von 1733.08.21). Der in Z\xfcrich lebende Adressat dieses Briefes kann also nicht Johann Jakob Scheuchzer sein. Der Adressat ist daher h\xf6chst wahrscheinlich dessen Bruder Johannes Scheuchzer.')


