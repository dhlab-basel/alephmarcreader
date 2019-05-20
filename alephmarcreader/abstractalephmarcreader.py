import abc

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class AbstractAlephMarcReader(ABC):

    class Person:
        """
        Represents a person.
        :param str|False name: the name of the person (family name, first name), if any.
        :param str|False lifespan: the lifespan of the person (year of birth and death separated by a '-'), if any.
        :param str|False gnd: the GND of the person, otherwise 'no_GND', if any.
        :param str|False role: the role of the person (author etc.), if any.

        """

        def __init__(self, name, lifespan, gnd, roles):
            self.name = name
            self.lifespan = lifespan
            self.gnd = gnd
            self.roles = roles

    class Organisation:
        """
        Represents a person.
        :param str|False name: the name of the person (family name, first name), if any.
        :param str|False gnd: the GND of the person, otherwise 'no_GND', if any.
        :param str|False role: the role of the person (author etc.), if any.
        :param str|False place the place of the organisation.
        :param str|False division of the organisation.
        """

        def __init__(self, name, gnd, roles, place, division):
            self.name = name
            self.gnd = gnd
            self.roles = roles
            self.place = place
            self.division = division

    class Place:
        """
        Represents a place.
        :param str|False name: the name of the place, if any.
        :param str|False gnd: the GND of the place, otherwise 'no_GND', if any.
        """

        def __init__(self, name, gnd):
            self.name = name
            self.gnd = gnd

    class Shelfmark:
        """
        Represents a shelfmark.
        :param str|False institution: the name of the institution, if any.
        :param str|False identifier: the identifier, if any.
        """
        def __init__(self, institution, identifier):
            self.institution = institution
            self.identifier = identifier

    class Description:
        """
        Represents the physical description.
        :param str extent: the extent of the manuscript, i.e. number of pages.
        :param str|False attribute: the attribute of the manuscript, if any.
        :param str|False dimension: the dimension of the manuscript, if any.
        :param str|False supplement: supplementary material, if any.
        """
        def __init__(self, extent, attribute, dimension, supplement):
            self.extent = extent
            self.attribute = attribute
            self.dimension = dimension
            self.supplement = supplement

    def __init__(self, gnd_index):
        """
        :param gnd_index: index of the GND subfield.
        """
        self._gnd_index = gnd_index

    @abc.abstractmethod
    def __get_subfield_texts(self, marc_field, index):
        pass

    @abc.abstractmethod
    def __get_field(self, index):
        pass

    def _handle_subfields_cardinality_max_one(self, subfields):
        """
        Handles subfields whose occurrence is max one (optional):
        - empty list -> False
        - one entry -> str
        :param [str] subfields: the subfields to handle
        :return: False | str
        """
        if len(subfields) == 1:
            return subfields[0]
        else:
            return False

    def _get_person_info(self, marc_field):
        """
        Extracts person information from a Marc field incl. the GND, if any.
        :param pymarc.field.Field marc_field: the Marc21 field that contains information about a person.
        :param str gnd_index: the index of the GND subfield.
        :return: Person
        """

        name = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(marc_field, 'a'))

        date = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(marc_field, 'd'))

        gnd = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(marc_field, self._gnd_index))
        if gnd:
            gnd = gnd.replace(',', '') # get rid of trailing comma

        # get rid of trailing comma in roles
        roles = list(map(lambda role: role.replace(',', ''), self.__get_subfield_texts(marc_field, '4')))

        return self.Person(name, date, gnd, roles)

    def _get_organisation_info(self, marc_field):
        """
        Extracts organisation info from a Marc field incl. the GND, if any.
        :return: [Organisation]
        """
        name = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(marc_field, 'a'))

        gnd = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(marc_field, self._gnd_index))
        if gnd:
            gnd = gnd.replace(',', '')  # get rid of trailing comma

        # get rid of trailing comma in roles
        roles = list(map(lambda role: role.replace(',', ''), self.__get_subfield_texts(marc_field, '4')))

        place = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(marc_field, 'g'))

        division = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(marc_field, 'b'))

        return self.Organisation(name, gnd, roles, place, division)


    def get_author(self):
        """
        Returns information about the author.
        :return: [Person]
        """
        author = []
        for field in self.__get_field('100'):
            author.append(self._get_person_info(field))

        # check for recipients (700) that are actually authors
        for field in self.__get_field('700'):
            person = self._get_person_info(field)

            if "aut" in person.roles:
                author.append(person)

        return author
    get_author.__annotations__ = {'return': [Person]}

    def get_recipient(self):
        """
        Returns information about the recipient.
        :return: [Person]
        """
        recipient = []
        for field in self.__get_field('700'):
            person = self._get_person_info(field)

            if "rcp" in person.roles:
                recipient.append(person)

        return recipient
    get_recipient.__annotations__ = {'return': [Person]}

    def get_mentioned_person(self):
        """
        Returns information about a mentioned person.
        :return: [Person]
        """
        mentioned = []
        for field in self.__get_field('600'):
            mentioned.append(self._get_person_info(field))

        return mentioned
    get_mentioned_person.__annotations__ = {'return': [Person]}

    def get_date(self):
        """
        Returns the date.
        :return: [str]
        """
        date = []
        for field in self.__get_field('046'):
            date_text = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'c'))

            if date_text:
                date.append(date_text)

        return date
    get_date.__annotations__ = {'return': [str]}

    def get_creation_place(self):
        """
        Returns the place of creation.
        :return: [Place]
        """
        creation_place = []

        for field in self.__get_field('751'):
            name = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'a'))

            gnd = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, self._gnd_index))

            cp = self.Place(name, gnd)
            creation_place.append(cp)

        return creation_place
    get_creation_place.__annotations__ = {'return': [Place]}

    def get_shelfmark(self):
        """
        Returns the shelfmark.
        :return: [Shelfmark]
        """
        shelfmark = []

        for field in self.__get_field('852'):
            institution = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'a'))

            identifier = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'p'))

            sm = self.Shelfmark(institution, identifier)
            shelfmark.append(sm)

        return shelfmark
    get_shelfmark.__annotations__ = {'return': [Shelfmark]}

    def get_general_remarks(self):
        """
        Returns the general remarks.
        :return: [str]
        """
        footnote = []

        for field in self.__get_field('500'):
            footnote_text = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'a'))

            if footnote_text:
                footnote.append(footnote_text)

        return footnote
    get_general_remarks.__annotations__ = {'return': [str]}

    def get_content_summary(self):
        """
        Returns the content summary.
        :return: [str]
        """
        summary = []

        for field in self.__get_field('520'):
            footnote_text = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'a'))

            if footnote_text:
                summary.append(footnote_text)

        return summary
    get_content_summary.__annotations__ = {'return': [str]}

    def get_emanuscripta_doi(self):
        """
        Returns the emanuscripta DOI.
        :return: [str]
        """
        external_link = []

        for field in self.__get_field('024'):
            ext_link = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'a'))

            if ext_link:
                external_link.append(ext_link)

        return external_link

    get_emanuscripta_doi.__annotations__ = {'return': [str]}

    def get_physical_description(self):
        """
        Returns the physical description.
        :return: [Description]
        """
        physical_description = []

        for field in self.__get_field('300'):
            extent = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'a'))
            attribute = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'b'))
            dimension = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'c'))
            supplement = self._handle_subfields_cardinality_max_one(self.__get_subfield_texts(field, 'e'))

            physical_description.append(self.Description(extent, attribute, dimension, supplement))

        return physical_description

    get_physical_description.__annotations__ = {'return': [Description]}

    def get_language(self):
        """
        Returns the language.
        :return: [str]
        """
        language = []

        for field in self.__get_field('041'):
            # subfield may occur several times
            lang = self.__get_subfield_texts(field, 'a')

            for lan in lang:
                language.append(lan)

        return language

    get_language.__annotations__ = {'return': [str]}

    def get_mentioned_organisation(self):
        """
        Returns the mentioned organisation.
        :return: [Organisation]
        """
        mentioned_organisation = []
        for field in self.__get_field('610'):
            mentioned_organisation.append(self._get_organisation_info(field))

        return mentioned_organisation

    get_mentioned_organisation.__annotations__ = {'return': [Organisation]}

    def get_recipient_organisation(self):
        """
        Returns the receiving organisation.
        :return: [Organisation]
        """
        recipient_organisation = []
        for field in self.__get_field('710'):
            org = self._get_organisation_info(field)

            if "rcp" in org.roles:
                recipient_organisation.append(org)

        return recipient_organisation

    get_recipient_organisation.__annotations__ = {'return': [Organisation]}