ECHO running unit tests

cd ..\..

ECHO Python v.2

py -2 -m unittest alephmarcreader.tests.test_Marc21Reader

py -2 -m unittest alephmarcreader.tests.test_MarcXMLReader

py -2 -m unittest alephmarcreader.tests.test_XReader

ECHO Python v.3

py -3 -m unittest alephmarcreader.tests.test_Marc21Reader

py -3 -m unittest alephmarcreader.tests.test_MarcXMLReader

py -3 -m unittest alephmarcreader.tests.test_XReader

PAUSE