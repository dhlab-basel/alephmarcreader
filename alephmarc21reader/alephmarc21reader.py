import pymarc
import codecs
import sys


class AlephMarc21Reader:
    """
    Represents the record read from a Marc21 file.
    :param pymarc.record.Record record record read from a Marc21 file.
    """
    def __init__(self, file_path):
        """
        :param str file_path: the path to the Marc21 file.
        """
        marc21 = self.__get_marc21(file_path)
        self.record = self.__get_record(marc21)

    def __get_marc21(self, file_path):
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

    def __get_record(self, marc21):
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

    class Person:
        """
        Represents a person.
        :param str name: the name of the person (family name, first name).
        :param str lifespan: the lifespan of the person (year of birth and death separated by a '-').
        :param str gnd: the GND of the person, otherwise 'no_GND'.
        :param str role: the role of the person (author etc.).

        """

        def __init__(self, name, lifespan, gnd, role):
            self.name = name
            self.lifespan = lifespan
            self.gnd = gnd
            self.role = role

    def __get_person_info(self, marc_field, gnd_index):
        """
        Extracts person information from a Marc field incl. the GND, if any.
        Returns a dictionary containing that information with they keys: GND, name, date, role.
        :param pymarc.field.Field marc_field: the Marc21 field that contains information about a person.
        :param str gnd_index: the index of the GND subfield.
        :return: Person
        """

        if marc_field['d'] is not None:
            date = marc_field['d']
        else:
            date = 'no_date'

        if marc_field[gnd_index] is None:
            GND = 'no_GND'
        else:
            # get rid of trailing comma
            GND = marc_field[gnd_index].replace(',', '')

        if marc_field['4'] is not None:
            role = marc_field['4']
        else:
            role = 'no_role'

        return AlephMarc21Reader.Person(marc_field['a'], date, GND, role)
    __get_person_info.__annotations__ = {'marc_field': pymarc.field.Field, 'gnd_index': str, 'return': Person}

    def get_author(self):
        """
        Returns author information from a Marc21 record.
        :return: Person
        """
        author = []
        for field in self.record.get_fields('100'):
            author.append(self.__get_person_info(field, '0'))

        # check for 700 that are actually authors
        for field in self.record.get_fields('700'):
            person = self.__get_person_info(field, '0')

            if person.role == "aut":
                author.append(person)

        return author
    get_author.__annotations__ = {'return': Person}