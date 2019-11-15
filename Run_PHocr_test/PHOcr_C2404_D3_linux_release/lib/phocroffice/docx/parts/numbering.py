# encoding: utf-8

"""
|NumberingPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.part import XmlPart
from phocr_shared.shared import lazyproperty


class NumberingPart(XmlPart):
    """
    Proxy for the numbering.xml part containing numbering definitions for
    a document or glossary.
    """
    @classmethod
    def new(cls):
        """
        Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element.
        """
        raise NotImplementedError

    @lazyproperty
    def numbering_definitions(self):
        """
        The |_NumberingDefinitions| instance containing the numbering
        definitions (<w:num> element proxies) for this numbering part.
        """
        return _NumberingDefinitions(self._element)

    def get_nums(self):
        """
        Get list of <w:num> contained in NumberingPart
        After initialize, this list contain all list in template docx file.
        :return: list of w:num
        """
        element = self._element
        if element is None:
            return None
        else:
            return element.num_lst

    def get_num(self, num_id):
        """
        Get exactlt <w:num> element bu numid
        :param num_id:
        :return: num_id that got from num_lst
        """
        element = self._element
        if element is None:
            return None
        else:
            xpath = './w:num[@w:numId="%d"]' % num_id
            try:
                return element.xpath(xpath)[0]
            except IndexError:
                raise KeyError('no <w:num> element with numId %d' % num_id)

    def add_num(self, abstractNum_id):
        """
        Add more <w:num> element to numbering definition, this num will
        refer to <w:asbtractNum> and use to override some information
        :param abstractNumId: abstractNum will be referred
        :return: new <w:num> element
        """
        element = self._element
        if element is None:
            return None
        else:
            return self._element.add_num(abstractNum_id)


class _NumberingDefinitions(object):
    """
    Collection of |_NumberingDefinition| instances corresponding to the
    ``<w:num>`` elements in a numbering part.
    """
    def __init__(self, numbering_elm):
        super(_NumberingDefinitions, self).__init__()
        self._numbering = numbering_elm

    def __len__(self):
        return len(self._numbering.num_lst)
