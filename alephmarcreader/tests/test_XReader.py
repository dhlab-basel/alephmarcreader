import unittest

from alephmarcreader import AlephXReader

class TestMethods(unittest.TestCase):
    def test_author(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000055275.xml')

        author = marcx_rd.get_author()

        self.assertEqual(len(author), 1)

        self.assertEqual(author[0].name, u'Bernoulli, Daniel')
        self.assertEqual(author[0].lifespan, u'1700-1782')
        self.assertEqual(author[0].gnd, u'(DE-588)118656503')
        self.assertEqual(author[0].roles, [u'aut'])

    def test_recipient(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000055275.xml')

        recipient = marcx_rd.get_recipient()

        self.assertEqual(len(recipient), 1)

        self.assertEqual(recipient[0].name, u'Scheuchzer, Johann')
        self.assertEqual(recipient[0].lifespan, u'1684-1738')
        self.assertEqual(recipient[0].gnd, u'(DE-588)120379260')
        self.assertEqual(recipient[0].roles, [u'rcp'])

    def test_mentioned_person(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000055275.xml')

        mentioned = marcx_rd.get_mentioned_person()

        self.assertEqual(len(mentioned), 6)

        self.assertEqual(mentioned[0].name, u'Bernoulli, Johann')
        self.assertEqual(mentioned[0].lifespan, u'1667-1748')
        self.assertEqual(mentioned[0].gnd, u'(DE-588)118509969')
        self.assertEqual(mentioned[0].roles, [])

    def test_date(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000055275.xml')

        date = marcx_rd.get_date()

        self.assertEqual(len(date), 1)

        self.assertEqual(date[0], u'1734.03.12')

    def test_creation_place(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000055275.xml')

        cp = marcx_rd.get_creation_place()

        self.assertEqual(len(cp), 1)

        self.assertEqual(cp[0].name, u'Basel')
        self.assertEqual(cp[0].gnd, u'(DE-588)4004617-5')

    def test_get_shelfmark(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000055275.xml')

        sm = marcx_rd.get_shelfmark()

        self.assertEqual(len(sm), 1)

        self.assertEqual(sm[0].institution, u'ZB Z\xfcrich')
        self.assertEqual(sm[0].identifier, u'Ms H 340, pp. 569-572')

    def test_get_footnote(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000055275.xml')

        footnote = marcx_rd.get_general_remarks()

        self.assertEqual(len(footnote), 1)

        self.assertEqual(footnote[0], u'Die Briefhandschrift findet sich in einem Z\xfcricher Briefband mit der Aufschrift "Epistolae Helvetorum ad J. J. Scheuchzer". Johann Jakob Scheuchzer starb jedoch am 23.6.1733. Daniel Bernoulli hatte von dessen Tod sp\xe4testens im August 1733 auf der R\xfcckreise von St. Petersburg erfahren (s. Brief von Johann II Bernoulli an Leonhard Euler von 1733.08.21). Der in Z\xfcrich lebende Adressat dieses Briefes kann also nicht Johann Jakob Scheuchzer sein. Der Adressat ist daher h\xf6chst wahrscheinlich dessen Bruder Johannes Scheuchzer.')

    def test_recipient_with_multiple_roles(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000059794.xml')

        recipient = marcx_rd.get_recipient()

        self.assertEqual(len(recipient), 1)

        self.assertEqual(recipient[0].name, u'Hermann, Jacob')
        self.assertEqual(recipient[0].lifespan, u'1678-1733')
        self.assertEqual(recipient[0].gnd, u'(DE-588)119112450')
        self.assertEqual(recipient[0].roles, [u'scr', u'rcp'])

    def test_get_external_link(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000307927.xml')

        external_links = marcx_rd.get_emanuscripta_doi()

        self.assertEqual(len(external_links), 1)

        self.assertEqual(external_links[0], u'10.7891/e-manuscripta-39903')

    def test_get_pyhsical_description(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000059552.xml')

        physical_desc = marcx_rd.get_physical_description()

        self.assertEqual(len(physical_desc), 1)

        self.assertEqual(physical_desc[0].extent, u'3 S.')
        self.assertEqual(physical_desc[0].attribute, u'Fotokopie')
        self.assertEqual(physical_desc[0].dimension, u'22 x 16,5 cm')
        self.assertEqual(physical_desc[0].supplement, u'1 Beil.')

    def test_get_content_summary(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000059552.xml')

        content = marcx_rd.get_content_summary()

        self.assertEqual(len(content), 1)

        self.assertEqual(content[0], u'Nic. II B. antwortet versp\xe4tet auf einen Brief de Brui\xe8res, da er dessen Adresse erst von dessen Advokaten, M. Polin, erfragen musste. Er hat Brui\xe8re "au Faucon" besucht, ihn aber nicht angetroffen. Brui\xe8re hat ihn in seinem Brief um Aukl\xe4rung in einer bestimmten Sache gebeten. Von Polin hat Nic. II B. erfahren, dass es sich um das Dividieren handelt. Polin hat ihm aber dies bereits selbst erl\xe4utert.')

    def test_get_content_summary(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000054774.xml')

        lang = marcx_rd.get_language()

        self.assertEqual(len(lang), 2)

        self.assertEqual(lang[0], u'fre')
        self.assertEqual(lang[1], u'lat')

    def test_get_mentioned_organisation(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000307927.xml')

        mentioned_organisation = marcx_rd.get_mentioned_organisation()

        self.assertEqual(len(mentioned_organisation), 2)

        self.assertEqual(mentioned_organisation[0].name, u'Eck, van & c.')
        self.assertEqual(mentioned_organisation[0].gnd, False)
        self.assertEqual(mentioned_organisation[0].place, u'London')

        self.assertEqual(mentioned_organisation[1].name, u'Lefort Beaumont')
        self.assertEqual(mentioned_organisation[1].gnd, u'(DE-588)1086218213')
        self.assertEqual(mentioned_organisation[1].place, u'Gen\xe8ve')

    def test_get_recipient_organisation(self):
        marcx_rd = AlephXReader('alephmarcreader/tests/sample_data/AlephX/000056870.xml')

        mentioned_organisation = marcx_rd.get_recipient_organisation()

        self.assertEqual(len(mentioned_organisation), 2)

        self.assertEqual(mentioned_organisation[0].name, u'Universit\xe4t Basel')
        self.assertEqual(mentioned_organisation[0].gnd, u'(DE-588)1085854191')
        self.assertEqual(mentioned_organisation[0].roles, [u'rcp'])
        self.assertEqual(mentioned_organisation[0].division, u'Regenz')

        self.assertEqual(mentioned_organisation[1].name, u'Universit\xe4t Basel')
        self.assertEqual(mentioned_organisation[1].gnd, u'(DE-588)1087006392')
        self.assertEqual(mentioned_organisation[1].roles, [u'rcp'])
        self.assertEqual(mentioned_organisation[1].division, u'Rektorat')