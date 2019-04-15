from pymarc import MARCReader
import codecs
import sys

def get_marc21(file_path):
    """
    Returns the contents of a Marc21 file.
    :param str sys_id: the sys_id of the item to query for.
    :rtype: bytes
    """

    try:
        marc_file = codecs.open(file_path, 'rb')
        marc21 = marc_file.read()
        marc_file.close()

        return marc21

    except Exception as e:
        sys.stderr.write("Getting Marc21 failed: " + str(e) + " for file_path: " + file_path + "\n")
        exit(1)
get_marc21.__annotations__ = {'sys_id': str, 'return': bytes}

def get_records(marc21):
    """
    Parses the given Marc21 data and returns all its records as an instance of MARCReader.
    :param bytes marc21: Marc21 data.
    :rtype: MARCReader
    """

    try:
        reader = MARCReader(marc21, force_utf8=True, to_unicode=True)
        return next(reader)
    except Exception as e:
        sys.stderr.write("Error reading Marc21 data.")
        sys.stderr.write(str(e))
        exit(2)
get_records.__annotations__ = {'marc21': bytes, 'return': MARCReader}

def __check_for_gnd(marcField, GNDIndex):

    if marcField['d'] is not None:
        date = marcField['d']
    else:
        date = ''

    if marcField[GNDIndex] is None:
        GND = 'no_GND'
    else:
        # get rid of trailing comma
        GND = marcField[GNDIndex].replace(',', '')

    if marcField['4'] is not None:
        role = marcField['4']
    else:
        role = ''

    return {
        "GND": GND,
        "name": marcField['a'],
        "date": date,
        "role": role
    }

def get_author(records):
    author = []
    for field in records.get_fields('100'):
        author.append(__check_for_gnd(field, '0'))

    # check for 700 that are actually authors
    for field in records.get_fields('700'):
        person = __check_for_gnd(field, '0')

        if person['role'] == "aut":
            author.append(person)

    return author