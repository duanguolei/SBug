"""
code speace
@Time    : 2024/3/17 15:28
@Author  : 泪懿:dgl
@File    : utils.py
"""
import re
import emoji
def has_emoji(text):
    return any( emoji.is_emoji(char) for char in text)




