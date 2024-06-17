"""
code speace
@Time    : 2024/3/7 16:36
@Author  : 泪懿:dgl
@File    : bookstrapform.py
"""
class BootStrapForm(object):
    bookstrap_class_exclude=[]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bookstrap_class_exclude:
                continue
            if field.widget.attrs.get('class'):
                field.widget.attrs['class']=field.widget.attrs.get('class')+' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)

