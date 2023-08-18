from PyQt5.QtGui import QColor

style = ""
#theme = "green.qss"
theme = "grey.qss"

green_chart_styles = {
    "title_font_size": 18,
    "title_bold": True,
    "title_color": 0x000000,
    "chart_background_color":   0xFAFFFA,
    "plot_area_bkg_brush":      0xFAFFFA,
    "legend_font_size": 12,
    "legend_italic": True,
    "legend_visible": True,
    "legend_color": 0x000000,
    "series_line_color": 0xff0000,
    "series_line_width": 3,
    "axis_color": 0x00000,
    "axis_width": 2,
    "label_color": 0x000000,
    "label_font_size": 10,
    "grid_line_color": 0xaaaaaa,
    "grid_shade_color": 0xeeffee,
    "grid_shades_visible": True,
    "grid_line_visible": True,

    "axis_title_font_size": 14,
    "axis_title_italic": True,
    "axis_title_bold": True,
    "axis_title_color": 0x000000,
}

grey_chart_styles = {
    "title_font_size": 18,
    "title_bold": True,
    "title_color": 0x848688,
    "chart_background_color":   0x4B4B4D,
    "plot_area_bkg_brush":      0x373435,
    "legend_font_size": 12,
    "legend_italic": True,
    "legend_visible": True,
    "legend_color": 0x848688,
    "series_line_color": 0xE6E7E8,
    "series_line_width": 3,
    "axis_color": 0x848688,
    "axis_width": 2,
    "label_color": 0x848688,
    "label_font_size": 10,
    "grid_line_color": 0x727376,
    "grid_shade_color": 0x4B4B4D,
    "grid_shades_visible": True,
    "grid_line_visible": True,
    "axis_title_font_size": 14,
    "axis_title_italic": True,
    "axis_title_bold": True,
    "axis_title_color": 0x848688,

}

#chart_styles = green_chart_styles
chart_styles = grey_chart_styles

def init():
    global  style
    f = open(theme, "r")
    style = f.read()
