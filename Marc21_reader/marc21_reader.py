import pymarc
import codecs
import sys

def get_marc21(file_path):
    """
    Returns the contents of a Marc21 file as binary data.
    :param str file_path: the path to the Marc21 file.
    :return: bytes
    """

    try:
        marc_file = codecs.open(file_path, 'rb')
        marc21 = marc_file.read()
        marc_file.close()

        return marc21

    except Exception as e:
        sys.stderr.write("Getting Marc21 failed: " + str(e) + " for file_path: " + file_path + "\n")
        exit(1)
get_marc21.__annotations__ = {'file_path': str, 'return': bytes}

def get_record(marc21):
    """
    Parses the given Marc21 data and returns the record.
    :param bytes marc21: Marc21 data.
    :return: pymarc.record.Record
    """
    try:
        reader = pymarc.MARCReader(marc21, force_utf8=True, to_unicode=True)
        return next(reader)
    except Exception as e:
        sys.stderr.write("Error reading Marc21 data: ")
        sys.stderr.write(str(e))
        exit(2)
get_record.__annotations__ = {'marc21': bytes, 'return': pymarc.record.Record}

def __check_for_gnd(marcField, GNDIndex):
    """
    Extracts person information from a Marc field incl. the GND, if any.
    Returns a dictionary containing that information with they keys: GND, name, date, role.
    :param pymarc.field.Field marcField: the Marc field that contains information about a person.
    :param str GNDIndex:
    :return: dict
    """

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
__check_for_gnd.__annotations__ = {'marcField': pymarc.field.Field, 'return': dict}

def get_author(record):
    """
    Returns author information from a Marc record as a dictionary.
    :param pymarc.record.Record record: the Marc record to get the author information from.
    :return: dict
    """
    author = []
    for field in record.get_fields('100'):
        author.append(__check_for_gnd(field, '0'))

    # check for 700 that are actually authors
    for field in record.get_fields('700'):
        person = __check_for_gnd(field, '0')

        if person['role'] == "aut":
            author.append(person)

    return author
get_author.__annotations__ = {'record': pymarc.record.Record, 'return': dict}