# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from pptx.enum.bullet import MSO_BULLET_CHARACTER, MSO_BULLET_NUMBERING
from phocr_shared.phocr_common import DocumentType, CoordinateTransform
from phocr_shared.shared import Pt, Inches
from docx.enum.text import WD_TAB_ALIGNMENT, WD_PARAGRAPH_ALIGNMENT
from phocr_shared.alignment import string_to_alignment_docx

MIN_TAB_SIZE = int(914400 * 0.2)
MAX_TAB_SIZE = int(914400 * 2)
DEFAULT_TAB_SIZE = int(914400 * 0.25)


class NumberingType:
    ARABIC_NON_SUFFIX = 'ARABIC_NON_SUFFIX'
    ARABIC_PERIOD = 'ARABIC_PERIOD'
    ARABIC_PAREN_R = 'ARABIC_PAREN_R'
    ALPHA_LC_PERIOD = 'ALPHA_LC_PERIOD'
    ALPHA_UC_PERIOD = 'ALPHA_UC_PERIOD'
    ALPHA_LC_PAREN_R = 'ALPHA_LC_PAREN_R'
    ROMAN_LC_PERIOD = 'ROMAN_LC_PERIOD'
    ROMAN_UC_PERIOD = 'ROMAN_UC_PERIOD'


class BulletType:
    HOLLOW_ROUND = 'HOLLOW_ROUND'
    FILLED_ROUND = 'FILLED_ROUND'


class BULLET_NUMBERING:
    BULLET = 'BULLET'
    NUMBERING = 'NUMBERING'


class NumFormat:
    UPPER_LETER = 'upperLetter'
    LOWER_LETTER = 'lowerLetter'
    LOWER_ROMAN = 'lowerRoman'
    UPPER_ROMAN = 'upperRoman'


class NumText:
    PAREN = '%1)'
    PERIOD = '%1.'
    NON_SUFFIX = '%1'


class StyleName:
    List_Bullet = 'List Bullet'
    List_Bullet_2 = 'List Bullet 2'
    List_Bullet_3 = 'List Bullet 3'
    List_Number = 'List Number'
    List_Number_2 = 'List Number 2'
    List_Number_3 = 'List Number 3'


class BulletNumberingContainer:
    def __init__(self):
        self.elements = []

    def get_last(self):
        """
        Get last element of list
        :return:
        """
        if len(self.elements) == 0:
            return None
        return self.elements[-1]

    def insert_new(self, bullet_numbering):
        """
        Append new element at the end of list
        :param bullet_numbering: numbering will be stored
        :return:
        """
        self.elements.append(bullet_numbering)

    def get_length(self):
        """
        Get size of list contain bullet numbering object
        :return:
        """
        return len(self.elements)


class BulletNumbering:
    def __init__(self):
        self.list_type = None
        self.start_at = -1
        self.list_level = -1
        self.list_name = ''
        self.container = BulletNumberingContainer()

    def get_container(self):
        return self.container


def push_bullet_numbering_to_container(container, bullet_numbering):
    """
    Push new element to container by following level
    :param container: list contain bullet numbering objects
    :param bullet_numbering: object that we want to push
    :return:
    """
    current_container = container
    while True:
        if current_container.get_length() == 0:
            current_container.insert_new(bullet_numbering)
            break
        else:
            last_bullet_numbering = current_container.get_last()
            if last_bullet_numbering is not None and \
                    bullet_numbering.list_level == last_bullet_numbering.list_level:
                current_container.insert_new(bullet_numbering)
                break
            else:
                current_container = last_bullet_numbering.get_container()


def get_last_same_from_container(container, bullet_numbering):
    """
    Get last element have level same with bullet_numbering's level
    :param container: container that we want to get
    :param bullet_numbering:
    :return:
    """
    current_container = container
    while True:
        if current_container.get_length() == 0:
            return None
        else:
            last_bullet_numbering = current_container.get_last()
            if last_bullet_numbering.list_level == bullet_numbering.list_level and \
                    last_bullet_numbering.list_name == bullet_numbering.list_name:
                return last_bullet_numbering
            else:
                current_container = last_bullet_numbering.get_container()


def get_last_from_container(container):
    """
    Get last element from container, don't care about level
    :param container:
    :return:
    """
    current_container = container
    while True:
        if current_container.get_length() == 0:
            return None
        else:
            last_bullet_numbering = current_container.get_last()
            child_container = last_bullet_numbering.get_container()
            if child_container.get_length() == 0:
                return last_bullet_numbering
            else:
                current_container = child_container


def get_bullet_and_numbering_type(list_type, list_name):
    """
    Return Bullet or Numbering type from it's information.

    :param list_type: bullet or numbering
    :param list_name: detail name of bullet or numbering
    :return: exactly bullet or numbering type
    """

    list_name_ = None
    if list_type == BULLET_NUMBERING.BULLET:
        # We can't detect bullets type now, so we will set it as default
        # In future, if we have enough information, we will update it
        if list_name == BulletType.HOLLOW_ROUND:
            list_name_ = MSO_BULLET_CHARACTER.HOLLOW_ROUND
        else:
            list_name_ = MSO_BULLET_CHARACTER.FILLED_ROUND
    elif list_type == BULLET_NUMBERING.NUMBERING:
        if list_name == NumberingType.ALPHA_UC_PERIOD:
            list_name_ = MSO_BULLET_NUMBERING.ALPHA_UC_PERIOD
        elif list_name == NumberingType.ALPHA_LC_PERIOD:
            list_name_ = MSO_BULLET_NUMBERING.ALPHA_LC_PERIOD
        else:
            # Currently, we don't have more information, so we can't detect
            # numbering type exactly
            # So we will set as default, maybe update in future.
            list_name_ = MSO_BULLET_NUMBERING.ARABIC_PERIOD
    if list_name_:
        return list_name_
    else:
        return MSO_BULLET_CHARACTER.FILLED_ROUND


def calculate_tab_size(creator, paragraph, override_lvl, alignment, converter,
                       is_near_image=None, text_box_rectangle=None):
    """
    This function will calculate size of tab character in bullet or numbering
    paragraphs and set to bullet or numbering properties.
    :param paragraph: paragraph xml element
    :param creator: word_creator
    :param converter: Pixel of docx or pptx module
    :param override_lvl: <w:lvlOverride> element
    :return:
    """
    if alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT and \
            len(paragraph.lines) == 1 and text_box_rectangle is not None:
        ppr = override_lvl.add_pPr()
        ppr.add_tab(WD_TAB_ALIGNMENT.NUM, DEFAULT_TAB_SIZE)
        return

    first_line = paragraph.lines[0]
    if len(first_line.words) < 2:
        return
    second_word_x = float(CoordinateTransform.getX(first_line.words[1],
                                                   creator.text_direction))
    if text_box_rectangle is not None:
        tab_size = converter(second_word_x, creator.dpi.horizontal_resolution) - text_box_rectangle.x
    else:
        tab_size = converter((second_word_x - creator.margin_left), creator.dpi.horizontal_resolution)
    if tab_size > 0:
        if tab_size < MIN_TAB_SIZE:
            tab_size = MIN_TAB_SIZE
        ppr = override_lvl.add_pPr()
        if is_near_image and tab_size > MAX_TAB_SIZE and \
                text_box_rectangle is None:
            ppr.add_tab(WD_TAB_ALIGNMENT.NUM, MIN_TAB_SIZE)
        else:
            ppr.add_tab(WD_TAB_ALIGNMENT.NUM, tab_size)


def update_bullets_and_numbering(creator, document, p,
                                 paragraph, carea_x, converter,
                                 is_near_image=None, text_box_rectangle=None):
    """
    This function will get information from xml to set to p object
    Currently, we only support some type that PHOcr can detect. We can implement
    another type in future.
    :param document: the object will call it, maybe WordCreator, PowerPointCreator
    or ExcelCreator
    :param p: paragraph object
    :param paragraph: paragraph that are get from xml
    :param converter: converter use to convert from inches to emu
    :param text_box_rectangle: contain textbox dimension
    :return: True if p are set bullet or numbering successful
    """
    bullet_numberings_container = creator.bullet_numberings
    bn = BulletNumbering()
    list_type = paragraph.list_type
    list_name = paragraph.list_name
    bn.list_type = list_type
    bn.start_at = paragraph.start_at
    bn.list_name = list_name

    if bn.list_type != BULLET_NUMBERING.BULLET and \
            bn.list_type != BULLET_NUMBERING.NUMBERING:
        return False

    list_level = paragraph.list_level
    if list_level:
        bn.list_level = int(list_level)
        p.level = bn.list_level

    last_bn_same_level = get_last_same_from_container(
        bullet_numberings_container,
        bn
    )
    last_bullet_numbering = get_last_from_container(bullet_numberings_container)

    p.margin_left = converter(paragraph.x - carea_x, creator.dpi.horizontal_resolution)

    if len(paragraph.lines) == 0:
        return False
    first_line = paragraph.lines[0]
    word_x_fsize = 0
    if len(first_line.words) > 0:
        p.indent = converter((first_line.words[1].x - paragraph.x), creator.dpi.horizontal_resolution)
        word_x_fsize = float(first_line.words[0].size)

    # Set bullet and numbering for pptx file
    if creator.document_type == DocumentType.PPTX:
        if bn.list_type == BULLET_NUMBERING.BULLET:
            p.bullet_character = get_bullet_and_numbering_type(
                bn.list_type, list_name
            )
            p.bullet_font = 'Courier New'
        if bn.list_type == BULLET_NUMBERING.NUMBERING:
            p.bullet_number = get_bullet_and_numbering_type(
                bn.list_type, list_name
            )
            p.bullet_font = '+mj-lt'
            p.bullet_start_number = bn.start_at

    # Set bullet and numbering for docx file
    elif creator.document_type == DocumentType.DOCX:
        numbering = document.numberings
        alignment = string_to_alignment_docx(paragraph.alignment)
        if bn.list_type == BULLET_NUMBERING.BULLET:
            if bn.list_level == 0:
                p.style = StyleName.List_Bullet
            elif bn.list_level == 1:
                p.style = StyleName.List_Bullet_2
            elif bn.list_level >= 2:
                p.style = StyleName.List_Bullet_3

            if last_bullet_numbering is not None and \
                    creator.is_list_para and \
                    bn.list_level == \
                    last_bullet_numbering.list_level and \
                    bn.list_name == last_bullet_numbering.list_name:
                p.paragraph_format.num_id = last_bullet_numbering.num_id
            else:
                # get numid from document part or style part
                num_id = p.paragraph_format.num_id
                if num_id is None:
                    num_id = p.style.paragraph_format.num_id
                # get Abstract ID to refer
                num = numbering.get_num(num_id)
                abtract_num = num.abstractNum_id

                # create new num
                num_new = numbering.add_num(abtract_num)

                override = num_new.add_lvlOverride(0)
                override_lvl = override.add_lvl(0)
                calculate_tab_size(creator, paragraph, override_lvl, alignment,
                                   converter, is_near_image, text_box_rectangle)

                if list_name == BulletType.HOLLOW_ROUND:
                    override_lvl.add_lvlText('o')
                    rpr = override_lvl.add_rPr()
                    rpr.rFonts_ascii = 'Courier New'
                else:
                    # set filled bullet as default
                    override_lvl.add_lvlText(u'•')

                # set num id that created to paragraph format
                p.paragraph_format.num_id = num_new.num_id
        elif bn.list_type == BULLET_NUMBERING.NUMBERING:
            if bn.list_level == 0:
                p.style = StyleName.List_Number
            elif bn.list_level == 1:
                p.style = StyleName.List_Number_2
            elif bn.list_level >= 2:
                p.style = StyleName.List_Number_3
            if last_bn_same_level is not None and \
                    bn.start_at - last_bn_same_level.start_at == 1 and \
                    bn.list_name == last_bn_same_level.list_name and \
                    bn.list_level == last_bn_same_level.list_level:
                # don't create new num
                p.paragraph_format.num_id = last_bn_same_level.num_id
            else:
                num_id = p.paragraph_format.num_id

                # get numid from document part or style part
                if num_id is None:
                    num_id = p.style.paragraph_format.num_id
                # get Abstract ID to refer
                num = numbering.get_num(num_id)
                abtract_num = num.abstractNum_id

                # create new num
                num_new = numbering.add_num(abtract_num)

                override = num_new.add_lvlOverride(0)
                override.add_startOverride(bn.start_at)

                override_lvl = override.add_lvl(0)
                # Set font size for numbering character. Font name is default
                rpr = override_lvl.add_rPr()
                rpr.rFonts_ascii = 'Courier New'
                rpr.sz_val = Pt(word_x_fsize)

                # Fix tab size of numbering
                calculate_tab_size(creator, paragraph, override_lvl, alignment,
                                   converter, is_near_image, text_box_rectangle)
                if list_name == NumberingType.ARABIC_NON_SUFFIX:
                    override_lvl.add_lvlText(NumText.NON_SUFFIX)
                elif list_name == NumberingType.ARABIC_PAREN_R:
                    override_lvl.add_lvlText(NumText.PAREN)
                elif list_name == NumberingType.ALPHA_LC_PERIOD:
                    override_lvl.add_lvlText(NumText.PERIOD)
                    override_lvl.add_numFmt(NumFormat.LOWER_LETTER)
                elif list_name == NumberingType.ALPHA_UC_PERIOD:
                    override_lvl.add_lvlText(NumText.PERIOD)
                    override_lvl.add_numFmt(NumFormat.UPPER_LETER)
                elif list_name == NumberingType.ALPHA_LC_PAREN_R:
                    override_lvl.add_lvlText(NumText.PAREN)
                    override_lvl.add_numFmt(NumFormat.LOWER_LETTER)
                elif list_name == NumberingType.ROMAN_LC_PERIOD:
                    override_lvl.add_lvlText(NumText.PERIOD)
                    override_lvl.add_numFmt(NumFormat.LOWER_ROMAN)
                elif list_name == NumberingType.ROMAN_UC_PERIOD:
                    override_lvl.add_lvlText(NumText.PERIOD)
                    override_lvl.add_numFmt(NumFormat.UPPER_ROMAN)
                else:
                    override_lvl.add_lvlText(NumText.PERIOD)

                # set num id that created to paragraph format
                p.paragraph_format.num_id = num_new.num_id
        p.paragraph_format.contextualSpacing = 0
        bn.num_id = p.paragraph_format.num_id
        push_bullet_numbering_to_container(bullet_numberings_container, bn)

    return True
