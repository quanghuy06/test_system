# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_page import OfficePage


class OfficeDocument(object):
    """
    This class contains information all pages from phocr
    """
    def __init__(self):
        self.pages = []
        # Number of horizontal pages inside document
        self.number_horizontal_pages = 0
        # Number of vertical pages inside document, default is often only 1,
        # maybe changed in future development
        self.number_vertical_pages = 1

    def parse_xml(self, xml_obj):
        for page_xml in xml_obj:
            page = OfficePage()
            page.parse_xml(page_xml)
            self.pages.append(page)
        # Update number of horizontal page inside document
        self.number_horizontal_pages = len(self.pages)

    def get_max_size_of_pages(self):
        """
        Some folks have asked about resizing one slide or changing
        the page orientation within a presentation.
        But PowerPoint isn't able to do that.
        All slides in a presentation are the same size and page orientation.
        So, to make sure that every thing will displayed,
        we'll use maximum width and height of pages by Inch
        """
        max_width = 0
        max_height = 0
        for page in self.pages:
            width_by_inch = page.w / float(page.dpi.horizontal_resolution)
            height_by_inch = page.h / float(page.dpi.vertical_resolution)
            if width_by_inch > max_width:
                max_width = width_by_inch
            if height_by_inch > max_height:
                max_height = height_by_inch
        return max_width, max_height

    def create_one_page(self):
        """
        Create Office document with only one page, my idea is we start from page
        number i, increase the "y" attribute of any element to the height of
        total previous page. After that, we merge all element inside that page
        to the first page. So that, we only have one page, this will help excel
        export in only one page.
        :return:
        """
        page_count = 0
        height_of_page = 0
        total_height = 0
        first_page = self.pages[0]
        while page_count < len(self.pages):
            page = self.pages[page_count]
            total_height += page.h
            # Start processing from page with index = 1
            if page_count > 0:
                # Step 1. Shift vertical position of target page
                page.shift_vertical_position(height_of_page)

                # Step 2. Append all elements in target page to the first page
                target_content_areas = page.careas
                target_tables = page.tables
                target_photos = page.photos
                first_page.add_carea(target_content_areas)
                first_page.add_table(target_tables)
                first_page.add_photo(target_photos)
                self.pages.remove(page)
            else:
                page_count += 1

            # Update height of page
            height_of_page += page.h


        # Update height of the only one page
        first_page.h = total_height
