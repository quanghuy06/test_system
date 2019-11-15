# encoding: utf-8

"""
Enumerations used for specifying bullet.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from .base import (
    XmlEnumeration, XmlMappedEnumMember
)

class MSO_BULLET_CHARACTER(XmlEnumeration):
    """
    Specifies type of bullet character.

    Example::

        from pptx.enum.bullet import MSO_BULLET_CHARACTER

        paragraph.bullet_character = MSO_BULLET_CHARACTER.FILLED_ROUND
    """

    __ms_name__ = 'MsoBulletCharacter'

    __url__ = ()

    __members__ = (
        XmlMappedEnumMember(
            'FILLED_ROUND', 0, '•', 'The filled round bullet.'
        ),
        XmlMappedEnumMember(
            'HOLLOW_ROUND', 1, 'o', 'The hollow round bullet.'
        ),
        XmlMappedEnumMember(
            'FILLED_SQUARE', 2, '§', 'The filled square bullet.'
        ),
        XmlMappedEnumMember(
            'HOLLOW_SQUARE', 3, 'q', 'The hollow square bullet.'
        ),
        XmlMappedEnumMember(
            'STAR', 4, 'v', 'The star bullet.'
        ),
        XmlMappedEnumMember(
            'ARROW', 5, 'Ø', 'The arrow bullet.'
        ),
        XmlMappedEnumMember(
            'CHECKMARK', 6, 'ü', 'The checkmark bullet.'
        ),
    )

class MSO_BULLET_NUMBERING(XmlEnumeration):
    """
    Specifies type of bullet numbering.

    Example::

        from pptx.enum.bullet import MSH_BULLET_NUMBERING

        paragraph.bullet_number = MSH_BULLET_NUMBERING.ALPHA_LC_PAREN_R
    """

    __ms_name__ = 'MsoBulletNumbering'

    __url__ = ()

    __members__ = (
        XmlMappedEnumMember(
            'NONE', 0, 'None', 'Specifies no bullet and numbering.'
        ),
        XmlMappedEnumMember(
            'ALPHA_LC_PAREN_R', 1, 'alphaLcParenR', 'The bullet and numbering starts by "a)".'
        ),
        XmlMappedEnumMember(
            'ALPHA_LC_PERIOD', 2, 'alphaLcPeriod', 'The bullet and numbering starts by "a.".'
        ),
        XmlMappedEnumMember(
            'ALPHA_UC_PERIOD', 3, 'alphaUcPeriod', 'The bullet and numbering starts by "A.".'
        ),
        XmlMappedEnumMember(
            'ARABIC_PAREN_R', 4, 'arabicParenR', 'The bullet and numbering starts by "1)".'
        ),
        XmlMappedEnumMember(
            'ARABIC_PERIOD', 5, 'arabicPeriod', 'The bullet and numbering starts by "1.".'
        ),
        XmlMappedEnumMember(
            'ROMAN_LC_PERIOD', 6, 'romanLcPeriod', 'The bullet and numbering starts by "i.".'
        ),
        XmlMappedEnumMember(
            'ROMAN_UC_PERIOD', 7, 'romanUcPeriod', 'The bullet and numbering starts by "I.".'
        ),
    )

