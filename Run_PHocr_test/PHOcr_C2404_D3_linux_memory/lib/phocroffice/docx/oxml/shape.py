# encoding: utf-8

"""
Custom element classes for shape-related elements like ``<w:inline>``
"""

from __future__ import division

import cgi
from . import parse_xml
from .ns import nsdecls
from .simpletypes import (
    ST_Coordinate, ST_DrawingElementId, ST_PositiveCoordinate,
    ST_RelationshipId, XsdString, XsdToken
)
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, OptionalAttribute, RequiredAttribute,
    ZeroOrOne
)
from phocr_shared.shared import Length, RGBColor


class CT_Blip(BaseOxmlElement):
    """
    ``<a:blip>`` element, specifies image source and adjustments such as
    alpha and tint.
    """
    embed = OptionalAttribute('r:embed', ST_RelationshipId)
    link = OptionalAttribute('r:link', ST_RelationshipId)


class CT_BlipFillProperties(BaseOxmlElement):
    """
    ``<pic:blipFill>`` element, specifies picture properties
    """
    blip = ZeroOrOne('a:blip', successors=(
        'a:srcRect', 'a:tile', 'a:stretch'
    ))


class CT_GraphicalObject(BaseOxmlElement):
    """
    ``<a:graphic>`` element, container for a DrawingML object
    """
    graphicData = OneAndOnlyOne('a:graphicData')


class CT_GraphicalObjectData(BaseOxmlElement):
    """
    ``<a:graphicData>`` element, container for the XML of a DrawingML object
    """
    pic = ZeroOrOne('pic:pic')
    wps = ZeroOrOne('wps:wsp')
    uri = RequiredAttribute('uri', XsdToken)


class CT_Inline(BaseOxmlElement):
    """
    ``<w:inline>`` element, container for an inline shape.
    """
    extent = OneAndOnlyOne('wp:extent')
    docPr = OneAndOnlyOne('wp:docPr')
    graphic = OneAndOnlyOne('a:graphic')

    @classmethod
    def new(cls, cx, cy, shape_id, pic):
        """
        Return a new ``<wp:inline>`` element populated with the values passed
        as parameters.
        """
        inline = parse_xml(cls._inline_xml())
        inline.extent.cx = cx
        inline.extent.cy = cy
        inline.docPr.id = shape_id
        inline.docPr.name = 'Picture %d' % shape_id
        inline.graphic.graphicData.uri = (
            'http://schemas.openxmlformats.org/drawingml/2006/picture'
        )
        inline.graphic.graphicData._insert_pic(pic)
        return inline

    @classmethod
    def new_pic_inline(cls, shape_id, rId, filename, cx, cy):
        """
        Return a new `wp:inline` element containing the `pic:pic` element
        specified by the argument values.
        """
        pic_id = 0  # Word doesn't seem to use this, but does not omit it
        pic = CT_Picture.new(pic_id, filename, rId, cx, cy)
        inline = cls.new(cx, cy, shape_id, pic)
        inline.graphic.graphicData._insert_pic(pic)
        return inline

    @classmethod
    def _inline_xml(cls):
        return (
            '<wp:inline %s>\n'
            '  <wp:extent cx="914400" cy="914400"/>\n'
            '  <wp:docPr id="666" name="unnamed"/>\n'
            '  <wp:cNvGraphicFramePr>\n'
            '    <a:graphicFrameLocks noChangeAspect="1"/>\n'
            '  </wp:cNvGraphicFramePr>\n'
            '  <a:graphic>\n'
            '    <a:graphicData uri="URI not set"/>\n'
            '  </a:graphic>\n'
            '</wp:inline>' % nsdecls('wp', 'a', 'pic', 'r')
        )


class CT_Anchor(BaseOxmlElement):
    """
    ``<wp:anchor>`` element, container for an anchor shape.
    """
    extent = OneAndOnlyOne('wp:extent')
    docPr = OneAndOnlyOne('wp:docPr')
    graphic = OneAndOnlyOne('a:graphic')

    @classmethod
    def new_photo(cls, shape_id, cx, cy, cw, ch, pic, wrap, inside_table):
        """
        Return a new ``<wp:inline>`` element populated with the values passed
        as parameters.
        """
        inline = parse_xml(cls._anchor_photo_xml(shape_id, cx, cy, cw, ch,
                                                 wrap, inside_table))
        inline.extent.cx = int(cw)
        inline.extent.cy = int(ch)
        inline.docPr.id = shape_id
        inline.docPr.name = 'Picture %d' % shape_id
        inline.graphic.graphicData.uri = (
            'http://schemas.openxmlformats.org/drawingml/2006/picture'
        )
        inline.graphic.graphicData._insert_pic(pic)
        return inline

    @classmethod
    def new_textbox(cls, shape_id, cx, cy, cw, ch, txbx):
        """
        Return a new ``<wp:inline>`` element populated with the values passed
        as parameters.
        """
        inline = parse_xml(cls._anchor_textbox_xml(shape_id, cx, cy, cw, ch))
        inline.docPr.id = shape_id
        inline.docPr.name = 'Text Box %d' % shape_id
        inline.graphic.graphicData.uri = (
            'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
        )
        inline.graphic.graphicData._insert_wps(txbx)
        return inline

    @classmethod
    def new_photo_anchor(cls, shape_id, rId, filename, photo):
        """
        Return a new `wp:anchor` element containing the `wps:wsp` element
        specified by the argument values.
        """
        cx = photo.x
        cy = photo.y
        cw = photo.w
        ch = photo.h
        wrap = photo.wrap
        inside_table = photo.inside_table
        pic_id = 0  # Word doesn't seem to use this, but does not omit it
        pic = CT_Picture.new(pic_id, filename, rId, cw, ch)
        anchor = cls.new_photo(shape_id, cx, cy, cw, ch, pic,
                               wrap, inside_table)
        anchor.graphic.graphicData._insert_pic(pic)
        return anchor

    @classmethod
    def new_textbox_anchor(cls, shape_id, textbox):
        cx = textbox.x
        cy = textbox.y
        cw = textbox.w
        ch = textbox.h
        paragraphs = textbox.paragraphs
        angle = textbox.angle
        txbx = CT_Textbox.new(cw, ch, paragraphs, angle)
        anchor = cls.new_textbox(shape_id, cx, cy, cw, ch, txbx)
        anchor.graphic.graphicData._insert_wps(txbx)
        return anchor

    @classmethod
    def _anchor_photo_xml(cls, shape_id, cx, cy, cw, ch, wrap, inside_table):
        wrap_tag = r'<wp:{wrap} wrapText="bothSides"/>'.format(wrap=wrap)
        if wrap == 'wrapHorizontal':
            wrap_tag = r'<wp:wrapTopAndBottom/>'
        if wrap == "wrapTight":
            wrap_tag = ('    <wp:wrapTight wrapText="bothSides">\n'
                        '      <wp:wrapPolygon edited="0">\n'
                        '        <wp:start x="0" y="0"/>\n'
                        '        <wp:lineTo x="0" y="21600"/>\n'
                        '        <wp:lineTo x="21600" y="21600"/>\n'
                        '        <wp:lineTo x="21600" y="0"/>\n'
                        '        <wp:lineTo x="0" y="0"/>\n'
                        '      </wp:wrapPolygon>\n'
                        '    </wp:wrapTight>\n'
                        )
        if inside_table is True:
            behind_doc = 0
        else:
            behind_doc = 1
        ac = (
            '<wp:anchor %s distT="0" distB="0" distL="91440" distR="91440" \
            simplePos="0" relativeHeight="' + str(shape_id) +\
            '" behindDoc="' + str(behind_doc) +\
            '" locked="0" layoutInCell="1" allowOverlap="1">\n'
            '  <wp:simplePos x="0" y="0"/>\n'
            '  <wp:positionH relativeFrom="page">\n'
            '    <wp:posOffset>' + str(cx) + '</wp:posOffset>\n'
            '  </wp:positionH>\n'
            '  <wp:positionV relativeFrom="page">\n'
            '    <wp:posOffset>' + str(cy) + '</wp:posOffset>\n'
            '  </wp:positionV>\n'
            '  <wp:extent cx="' + str(cw) + '" cy="' + str(ch) + '"/>\n'
            '  <wp:effectExtent l="0" t="0" r="0" b="0"/>\n'
            '  ' + wrap_tag + '\n'
            '  <wp:docPr id="666" name="unnamed"/>\n'
            '  <wp:cNvGraphicFramePr>\n'
            '    <a:graphicFrameLocks noChangeAspect="1"/>\n'
            '  </wp:cNvGraphicFramePr>\n'
            '  <a:graphic>\n'
            '    <a:graphicData uri="URI not set"/>\n'
            '  </a:graphic>\n'
            '</wp:anchor>'
        )
        return ac % nsdecls('wp', 'a', 'wps', 'r')

    @classmethod
    def _anchor_textbox_xml(cls, shape_id, cx, cy, cw, ch):
        ac = (
            '<wp:anchor %s distT="0" distB="0" distL="0" distR="0" \
            simplePos="0" relativeHeight="' + str(shape_id) +\
            '" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="1">\n'
            '  <wp:simplePos x="0" y="0"/>\n'
            '  <wp:positionH relativeFrom="page">\n'
            '    <wp:posOffset>' + str(cx) + '</wp:posOffset>\n'
            '  </wp:positionH>\n'
            '  <wp:positionV relativeFrom="page">\n'
            '    <wp:posOffset>' + str(cy) + '</wp:posOffset>\n'
            '  </wp:positionV>\n'
            '  <wp:extent cx="' + str(cw) + '" cy="' + str(ch) + '"/>\n'
            '  <wp:effectExtent l="0" t="0" r="0" b="0"/>\n'
            '  <wp:wrapNone/>\n'
            '  <wp:docPr id="666" name="unnamed"/>\n'
            '  <wp:cNvGraphicFramePr/>\n'
            '  <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">\n'
            '    <a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"/>\n'
            '  </a:graphic>\n'
            '</wp:anchor>'
        )
        return ac % nsdecls('wp', 'a', 'wps', 'r')


class CT_NonVisualDrawingProps(BaseOxmlElement):
    """
    Used for ``<wp:docPr>`` element, and perhaps others. Specifies the id and
    name of a DrawingML drawing.
    """
    id = RequiredAttribute('id', ST_DrawingElementId)
    name = RequiredAttribute('name', XsdString)


class CT_NonVisualPictureProperties(BaseOxmlElement):
    """
    ``<pic:cNvPicPr>`` element, specifies picture locking and resize
    behaviors.
    """


class CT_Picture(BaseOxmlElement):
    """
    ``<pic:pic>`` element, a DrawingML picture
    """
    nvPicPr = OneAndOnlyOne('pic:nvPicPr')
    blipFill = OneAndOnlyOne('pic:blipFill')
    spPr = OneAndOnlyOne('pic:spPr')

    @classmethod
    def new(cls, pic_id, filename, rId, cx, cy):
        """
        Return a new ``<pic:pic>`` element populated with the minimal
        contents required to define a viable picture element, based on the
        values passed as parameters.
        """
        pic = parse_xml(cls._pic_xml())
        pic.nvPicPr.cNvPr.id = pic_id
        pic.nvPicPr.cNvPr.name = filename
        pic.blipFill.blip.embed = rId
        pic.spPr.cx = int(cx)
        pic.spPr.cy = int(cy)
        return pic

    @classmethod
    def _pic_xml(cls):
        return (
            '<pic:pic %s>\n'
            '  <pic:nvPicPr>\n'
            '    <pic:cNvPr id="666" name="unnamed"/>\n'
            '    <pic:cNvPicPr/>\n'
            '  </pic:nvPicPr>\n'
            '  <pic:blipFill>\n'
            '    <a:blip/>\n'
            '    <a:stretch>\n'
            '      <a:fillRect/>\n'
            '    </a:stretch>\n'
            '  </pic:blipFill>\n'
            '  <pic:spPr>\n'
            '    <a:xfrm>\n'
            '      <a:off x="0" y="0"/>\n'
            '      <a:ext cx="914400" cy="914400"/>\n'
            '    </a:xfrm>\n'
            '    <a:prstGeom prst="rect"/>\n'
            '  </pic:spPr>\n'
            '</pic:pic>' % nsdecls('pic', 'a', 'r')
        )


class CT_Textbox(BaseOxmlElement):
    """
    ``<wps:wps>`` element, a DrawingML textbox ``<wps:txbx>``
    """
    spPr = OneAndOnlyOne('wps:spPr')

    @classmethod
    def new(cls, cw, ch, paragraphs, angle):
        """
        Return a new ``<wps:wps>`` element populated with the minimal
        contents required to define a viable paragraph element, based on the
        values passed as parameters.
        """
        txbx = parse_xml(cls._textbox_xml(cw, ch, paragraphs, angle))
        return txbx

    @classmethod
    def _textbox_xml(cls, cw, ch, paragraphs, angle):
        if angle == 'vert270' or angle == 'vert':
            txbx = (
                '<wps:wsp %s>\n'
                '  <wps:cNvSpPr txBox="1" />\n'
                '  <wps:spPr>\n'
                '    <a:xfrm>\n'
                '      <a:off x="0" y="0" />\n'
                '      <a:ext cx="' + str(cw) + '" cy="' + str(ch) + '" />\n'
                '    </a:xfrm>\n'
                '    <a:prstGeom prst="rect">\n'
                '      <a:avLst />\n'
                '    </a:prstGeom>\n'
                '    <a:noFill />\n'
                '    <a:ln>\n'
                '      <a:noFill />\n'
                '    </a:ln>\n'
                '  </wps:spPr>\n'
                '  <wps:txbx>\n'
                '    <w:txbxContent>\n'
                '%s'
                '    </w:txbxContent>\n'
                '  </wps:txbx>\n'
                '  <wps:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" vert="' + str(angle) + '">\n'
                '    <a:spAutoFit />\n'
                '  </wps:bodyPr>\n'
                '</wps:wsp>'
            )
            return txbx % (nsdecls('wps', 'a', 'w', 'r'), str(paragraphs))
        elif angle == ' rot="10800000"':
            txbx = (
                '<wps:wsp %s>\n'
                '  <wps:cNvSpPr txBox="1" />\n'
                '  <wps:spPr>\n'
                '    <a:xfrm' + str(angle) + '>\n'
                '      <a:off x="0" y="0" />\n'
                '      <a:ext cx="' + str(cw) + '" cy="' + str(ch) + '" />\n'
                '    </a:xfrm>\n'
                '    <a:prstGeom prst="rect">\n'
                '      <a:avLst />\n'
                '    </a:prstGeom>\n'
                '    <a:noFill />\n'
                '    <a:ln>\n'
                '      <a:noFill />\n'
                '    </a:ln>\n'
                '  </wps:spPr>\n'
                '  <wps:txbx>\n'
                '    <w:txbxContent>\n'
                '%s'
                '    </w:txbxContent>\n'
                '  </wps:txbx>\n'
                '  <wps:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" vert="horz">\n'
                '    <a:spAutoFit />\n'
                '  </wps:bodyPr>\n'
                '</wps:wsp>'
            )
            return txbx % (nsdecls('wps', 'a', 'w', 'r'), str(paragraphs))
        else:
            txbx = (
                '<wps:wsp %s>\n'
                '  <wps:cNvSpPr txBox="1" />\n'
                '  <wps:spPr>\n'
                '    <a:xfrm>\n'
                '      <a:off x="0" y="0" />\n'
                '      <a:ext cx="' + str(cw) + '" cy="' + str(ch) + '" />\n'
                '    </a:xfrm>\n'
                '    <a:prstGeom prst="rect">\n'
                '      <a:avLst />\n'
                '    </a:prstGeom>\n'
                '    <a:noFill />\n'
                '    <a:ln>\n'
                '      <a:noFill />\n'
                '    </a:ln>\n'
                '  </wps:spPr>\n'
                '  <wps:txbx>\n'
                '    <w:txbxContent>\n'
                '%s'
                '    </w:txbxContent>\n'
                '  </wps:txbx>\n'
                '  <wps:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" vert="horz">\n'
                '    <a:spAutoFit />\n'
                '  </wps:bodyPr>\n'
                '</wps:wsp>'
            )
            return txbx % (nsdecls('wps', 'a', 'w', 'r'), str(paragraphs))


class CT_PictureNonVisual(BaseOxmlElement):
    """
    ``<pic:nvPicPr>`` element, non-visual picture properties
    """
    cNvPr = OneAndOnlyOne('pic:cNvPr')


class CT_Point2D(BaseOxmlElement):
    """
    Used for ``<a:off>`` element, and perhaps others. Specifies an x, y
    coordinate (point).
    """
    x = RequiredAttribute('x', ST_Coordinate)
    y = RequiredAttribute('y', ST_Coordinate)


class CT_PositiveSize2D(BaseOxmlElement):
    """
    Used for ``<wp:extent>`` element, and perhaps others later. Specifies the
    size of a DrawingML drawing.
    """
    cx = RequiredAttribute('cx', ST_PositiveCoordinate)
    cy = RequiredAttribute('cy', ST_PositiveCoordinate)


class CT_PresetGeometry2D(BaseOxmlElement):
    """
    ``<a:prstGeom>`` element, specifies an preset autoshape geometry, such
    as ``rect``.
    """


class CT_RelativeRect(BaseOxmlElement):
    """
    ``<a:fillRect>`` element, specifying picture should fill containing
    rectangle shape.
    """


class CT_ShapeProperties(BaseOxmlElement):
    """
    ``<pic:spPr>`` element, specifies size and shape of picture container.
    """
    xfrm = ZeroOrOne('a:xfrm', successors=(
        'a:custGeom', 'a:prstGeom', 'a:ln', 'a:effectLst', 'a:effectDag',
        'a:scene3d', 'a:sp3d', 'a:extLst'
    ))

    @property
    def cx(self):
        """
        Shape width as an instance of Emu, or None if not present.
        """
        xfrm = self.xfrm
        if xfrm is None:
            return None
        return xfrm.cx

    @cx.setter
    def cx(self, value):
        xfrm = self.get_or_add_xfrm()
        xfrm.cx = value

    @property
    def cy(self):
        """
        Shape height as an instance of Emu, or None if not present.
        """
        xfrm = self.xfrm
        if xfrm is None:
            return None
        return xfrm.cy

    @cy.setter
    def cy(self, value):
        xfrm = self.get_or_add_xfrm()
        xfrm.cy = value


class CT_StretchInfoProperties(BaseOxmlElement):
    """
    ``<a:stretch>`` element, specifies how picture should fill its containing
    shape.
    """


class CT_Transform2D(BaseOxmlElement):
    """
    ``<a:xfrm>`` element, specifies size and shape of picture container.
    """
    off = ZeroOrOne('a:off', successors=('a:ext',))
    ext = ZeroOrOne('a:ext', successors=())

    @property
    def cx(self):
        ext = self.ext
        if ext is None:
            return None
        return ext.cx

    @cx.setter
    def cx(self, value):
        ext = self.get_or_add_ext()
        ext.cx = value

    @property
    def cy(self):
        ext = self.ext
        if ext is None:
            return None
        return ext.cy

    @cy.setter
    def cy(self, value):
        ext = self.get_or_add_ext()
        ext.cy = value
