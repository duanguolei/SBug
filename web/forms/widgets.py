"""
code speace
@Time    : 2024/3/10 17:19
@Author  : 泪懿:dgl
@File    : widgets.py
"""
from django.forms import RadioSelect
class ColorRadioSelect(RadioSelect):
    template_name = 'web/widgets/color_radio/radio.html'
    option_template_name= 'web/widgets/color_radio/radio_option.html'