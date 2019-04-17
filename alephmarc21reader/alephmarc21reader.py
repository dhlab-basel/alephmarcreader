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
        :param str|False name: the name of the person (family name, first name), if any.
        :param str|False lifespan: the lifespan of the person (year of birth and death separated by a '-'), if any.
        :param str|False gnd: the GND of the person, otherwise 'no_GND', if any.
        :param str|False role: the role of the person (author etc.), if any.

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

        if 'a' in marc_field:
            name = marc_field['a']
        else:
            name = False

        if 'd' in marc_field:
            date = marc_field['d']
        else:
            date = False

        if gnd_index in marc_field:
            # get rid of trailing comma
            gnd = marc_field[gnd_index].replace(',', '')
        else:
            gnd = False

        if '4' in marc_field:
            role = marc_field['4']
        else:
            role = False

        return AlephMarc21Reader.Person(name, date, gnd, role)
    __get_person_info.__annotations__ = {'marc_field': pymarc.field.Field, 'gnd_index': str, 'return': Person}

    def get_author(self):
        """
        Returns information about the author.
        :return: [Person]
        """
        author = []
        for field in self.record.get_fields('100'):
            author.append(self.__get_person_info(field, '0'))

        # check for recipients (700) that are actually authors
        for field in self.record.get_fields('700'):
            person = self.__get_person_info(field, '0')

            if person.role == "aut":
                author.append(person)

        return author
    get_author.__annotations__ = {'return': [Person]}

    def get_recipient(self):
        """
        Returns information about the recipient.
        :return: [Person]
        """
        recipient = []
        for field in self.record.get_fields('700'):
            person = self.__get_person_info(field, '0')

            if person.role == "rcp":
                recipient.append(person)

        return recipient
    get_recipient.__annotations__ = {'return': [Person]}

    def get_mentioned_person(self):
        """
        Returns information about a mentioned person.
        :return: [Person]
        """
        recipient = []
        for field in self.record.get_fields('600'):
            recipient.append(self.__get_person_info(field, '0'))

        return recipient
    get_mentioned_person.__annotations__ = {'return': [Person]}

    def get_date(self):
        """
        Returns the date.
        :return: [str]
        """
        date = []
        for field in self.record.get_fields('046'):
            if 'c' in field:
                date.append(field['c'])

        return date
    get_date.__annotations__ = {'return': [str]}

    class Place:
        """
        Represents a place.
        :param str|False name: the name of the place, if any.
        :param str|False gnd: the GND of the place, otherwise 'no_GND', if any.
        """

        def __init__(self, name, gnd):
            self.name = name
            self.gnd = gnd

    def get_creation_place(self):
        """
        Returns the place of creation.
        :return: [Place]
        """
        creation_place = []
        for field in self.record.get_fields('751'):
            if 'a' in field:
                name = field['a']
            else:
                name = False

            if '0' in field:
                gnd = field['0']
            else:
                gnd = False

            cp = AlephMarc21Reader.Place(name, gnd)
            creation_place.append(cp)
        return creation_place
    get_creation_place.__annotations__ = {'return': [Place]}

    class Shelfmark:
        """
        Represents a shelfmark.
        :param str|False institution: the name of the institution, if any.
        :param str|False identifier: the identifier, if any.
        """
        def __init__(self, institution, identifier):
            self.institution = institution
            self.identifier = identifier

    def get_shelfmark(self):
        """
        Returns the shelfmark.
        :return: [Shelfmark]
        """
        shelfmark = []
        for field in self.record.get_fields('852'):
            if 'a' in field:
                institution = field['a']
            else:
                institution = False

            if 'p' in field:
                identifier = field['p']
            else:
                identifier = False

            sm = AlephMarc21Reader.Shelfmark(institution, identifier)
            shelfmark.append(sm)
        return shelfmark
    get_shelfmark.__annotations__ = {'return': [Shelfmark]}

    def get_footnote(self):
        """
        Returns the footnote.
        :return: [str]
        """
        footnote = []
        for field in self.record.get_fields('500'):
            if 'a' in field:
                footnote.append(field['a'])

        return footnote
    get_footnote.__annotations__ = {'return': [str]}