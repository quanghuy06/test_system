import xlwt

def get_len_excel(str_len):
    return str_len*300

# Cell stype excel
base_style = xlwt.easyxf('font: name Arial')
base_str = 'font: name Arial'
header_style = xlwt.easyxf('font: name Arial, bold on; alignment: horizontal left')
header_str = 'font: name Arial, bold on; alignment: horizontal left'

xlwt.add_palette_colour("custom_1", 0x21)
xlwt.add_palette_colour("custom_2", 0x22)
xlwt.add_palette_colour("custom_3", 0x23)
xlwt.add_palette_colour("custom_4", 0x24)

def border_cell(style):
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    style.borders = borders
    return style

def fore_color_cell(style, color):
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map[color]
    style.pattern = pattern
    return style

def rebase_style(style):
    style = xlwt.easyxf('font: name Arial')
    return style

def rebase_header_style(style):
    style = xlwt.easyxf('font: name Arial, bold on; alignment: horizontal center')
    return style

def align_horz(style, align):
    alignment = xlwt.Alignment()
    if align == "right":
        alignment.horz = xlwt.Alignment.HORZ_RIGHT
    if align == "left":
        alignment.horz = xlwt.Alignment.HORZ_LEFT
    if align == "center":
        alignment.horz = xlwt.Alignment.HORZ_CENTER
    style.alignment = alignment
    return style

def color_text(style, color):
    font = xlwt.Font()
    font.colour_index = xlwt.Style.colour_map[color]
    style.font = font
    return style

# Optional style
base_style_1 = xlwt.easyxf(base_str)
border_cell(base_style_1)
align_horz(base_style_1, "left")

base_style_2 = xlwt.easyxf(base_str)
border_cell(base_style_2)
align_horz(base_style_2, "center")

base_style_3 = xlwt.easyxf(base_str)
border_cell(base_style_3)
align_horz(base_style_3, "right")

base_style_4 = xlwt.easyxf(base_str)
border_cell(base_style_4)
align_horz(base_style_4, "center")
color_text(base_style_4, "green")
fore_color_cell(base_style_4, "light_green")

base_style_5 = xlwt.easyxf(base_str)
border_cell(base_style_5)
align_horz(base_style_5, "center")
color_text(base_style_5, "red")
fore_color_cell(base_style_5, "light_orange")

header_style_1 = xlwt.easyxf(header_str)
border_cell(header_style_1)
fore_color_cell(header_style_1, "gray25")

header_style_2 = xlwt.easyxf(header_str)
align_horz(header_style_2, "center")
border_cell(header_style_2)
fore_color_cell(header_style_2, "gray25")

header_style_3 = xlwt.easyxf(header_str)
align_horz(header_style_3, "right")
border_cell(header_style_3)
fore_color_cell(header_style_3, "gray25")

percent_style = xlwt.easyxf(base_str)
border_cell(percent_style)
percent_style.num_format_str = r"0.00\%"

pos_percent_style = xlwt.easyxf(base_str)
border_cell(pos_percent_style)
pos_percent_style.num_format_str = r"0.0000\%"
color_text(pos_percent_style, "green")
fore_color_cell(pos_percent_style, "light_green")

neg_percent_style = xlwt.easyxf(base_str)
border_cell(neg_percent_style)
neg_percent_style.num_format_str = r"0.0000\%"
color_text(neg_percent_style, "red")
fore_color_cell(neg_percent_style, "light_orange")

number_style_1 = xlwt.easyxf(base_str)
border_cell(number_style_1)
number_style_1.num_format_str = "0.00"

pos_style = xlwt.easyxf(base_str)
border_cell(pos_style)
color_text(pos_style, "green")
fore_color_cell(pos_style, "light_green")

neg_style = xlwt.easyxf(base_str)
border_cell(neg_style)
color_text(neg_style, "red")
fore_color_cell(neg_style, "light_orange")

header_green_1 = xlwt.easyxf(header_str)
border_cell(header_green_1)
fore_color_cell(header_green_1, "custom_1")

header_green_2 = xlwt.easyxf(header_str)
align_horz(header_green_2, "center")
border_cell(header_green_2)
fore_color_cell(header_green_2, "custom_1")

base_orange_1 = xlwt.easyxf(base_str)
border_cell(base_orange_1)
fore_color_cell(base_orange_1, "custom_4")

base_orange_2 = xlwt.easyxf(base_str)
align_horz(base_orange_2, "center")
border_cell(base_orange_2)
fore_color_cell(base_orange_2, "custom_4")

percent_style_orange = xlwt.easyxf(base_str)
border_cell(percent_style_orange)
percent_style_orange.num_format_str = r"0.00\%"
fore_color_cell(percent_style_orange, "custom_4")

strenght_color_1 = "custom_2"
strenght_color_2 = "custom_3"

strenght_1_1 = xlwt.easyxf(base_str)
align_horz(strenght_1_1, "left")
border_cell(strenght_1_1)
fore_color_cell(strenght_1_1, strenght_color_1)

strenght_1_2 = xlwt.easyxf(base_str)
align_horz(strenght_1_2, "center")
border_cell(strenght_1_2)
fore_color_cell(strenght_1_2, strenght_color_1)

percent_strenght_1 = xlwt.easyxf(base_str)
border_cell(percent_strenght_1)
percent_strenght_1.num_format_str = r"0.00\%"
fore_color_cell(percent_strenght_1, strenght_color_2)

strenght_2_1 = xlwt.easyxf(base_str)
align_horz(strenght_2_1, "left")
border_cell(strenght_2_1)
fore_color_cell(strenght_2_1, strenght_color_1)

strenght_2_2 = xlwt.easyxf(base_str)
align_horz(strenght_2_2, "center")
border_cell(strenght_2_2)
fore_color_cell(strenght_2_2, strenght_color_1)

percent_strenght_2 = xlwt.easyxf(base_str)
border_cell(percent_strenght_2)
percent_strenght_2.num_format_str = r"0.00\%"
fore_color_cell(percent_strenght_2, strenght_color_2)
