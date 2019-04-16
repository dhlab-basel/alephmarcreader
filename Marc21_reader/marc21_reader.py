import pymarc
import codecs
import sys

def __get_marc21(file_path):
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
__get_marc21.__annotations__ = {'file_path': str, 'return': bytes}

def __get_record(marc21):
    """
    Parses the given Marc21 data and returns the record.
    :param bytes marc21: Marc21 data.
    :return: pymarc.record.Record
    """
    try:
        reader = pymarc.MARCReader(marc21, force_utf8=True, to_unicode=True)
        return next(reader)
    except Exception as e:
        sys.stderr.write("Error reading Marc21 data: " + str(e) + '\n')
        exit(1)
__get_record.__annotations__ = {'marc21': bytes, 'return': pymarc.record.Record}

def get_record_from_file(file_path):
    """
    Given the path to a Marc21 file, returns the record.
    :param str file_path: the path to the Marc21 file.
    :return: pymarc.record.Record
    """
    marc21 = __get_marc21(file_path)
    return __get_record(marc21)
get_record_from_file.__annotations__ = {'file_path': str, 'return': pymarc.record.Record}

class Person:
    """
    Represents a person.
    :param str name: the nameof the person (family name, first name).
    :param str lifespan: the lifespan of the person (year of birth and death separated by a '-').
    :param str gnd: the GND of the person, otherwise 'no_GND'.
    :param str role: the role of the person (author etc.).

    """
    def __init__(self, name, lifespan, gnd, role):
        self.name = name
        self.lifespan = lifespan
        self.gnd = gnd
        self.role = role

def __get_person_info(marcField, GNDIndex):
    """
    Extracts person information from a Marc field incl. the GND, if any.
    Returns a dictionary containing that information with they keys: GND, name, date, role.
    :param pymarc.field.Field marcField: the Marc field that contains information about a person.
    :param str GNDIndex:
    :return: Person
    """

    if marcField['d'] is not None:
        date = marcField['d']
    else:
        date = 'no_date'

    if marcField[GNDIndex] is None:
        GND = 'no_GND'
    else:
        # get rid of trailing comma
        GND = marcField[GNDIndex].replace(',', '')

    if marcField['4'] is not None:
        role = marcField['4']
    else:
        role = 'no_role'

    return Person(marcField['a'], date, GND, role)
__get_person_info.__annotations__ = {'marcField': pymarc.field.Field, 'return': Person}

def get_author(record):
    """
    Returns author information from a Marc21 record.
    :param pymarc.record.Record record: the Marc record to get the author information from.
    :return: Person
    """
    author = []
    for field in record.get_fields('100'):
        author.append(__get_person_info(field, '0'))

    # check for 700 that are actually authors
    for field in record.get_fields('700'):
        person = __get_person_info(field, '0')

        if person.role == "aut":
            author.append(person)

    return author
get_author.__annotations__ = {'record': pymarc.record.Record, 'return': Person}