# -*- coding: utf-8 -*-

import re


class Util(object):
    """
    tool methods
    """

    # camel_to_underline_regex = re.compile('([a-z])([A-Z])')
    camel_to_underline_regex = re.compile('(?<=[a-z])([A-Z])|(?<=[A-Z]{2})([A-Z][a-z])')

    def __init__(self):
        pass

    @classmethod
    def get_collection_name(cls, item_name):
        return cls.camel_to_underline(item_name).rtrip('_item')

    @classmethod
    def camel_to_underline(cls, camel_format_str):
        """
            驼峰命名格式转下划线命名格式
        """
        if isinstance(camel_format_str, str):
            # 1000000 耗时 36.642秒
            # return cls.camel_to_underline_regex.sub(lambda m: m.group(1) + '_' + m.group(2), camel_format_str).lower()
            return cls.camel_to_underline_regex.sub(lambda m: "_"+m.group(), camel_format_str).lower()
        else:
            print('param is not str')
            return None

    @staticmethod
    def camel_to_underline2(camel_format):
        """
            驼峰命名格式转下划线命名格式
        """
        underline_format = ''
        if isinstance(camel_format, str):
            if camel_format[0].islower():
                underline_format = camel_format[0]
            else:
                underline_format = camel_format[0].lower()
            for _s_ in camel_format[1:]:
                underline_format += _s_ if _s_.islower() else '_' + _s_.lower()
        return underline_format

    @staticmethod
    def underline_to_camel(underline_format):
        """
            下划线命名格式驼峰命名格式
        """
        camel_format = ''
        if isinstance(underline_format, str):
            for _s_ in underline_format.split('_'):
                camel_format += _s_.capitalize()
        return camel_format

if __name__ == '__main__':
    import time
    print "%.6f" % time.time()
    s_time = time.time()
    print Util.camel_to_underline('XiaomiAPPItemPSItem')
    for i in range(1000000): Util.camel_to_underline('XiaomiAppItem')
    e_time = time.time()
    print e_time
    print "%.6f" % (e_time-s_time)
    print Util.underline_to_camel('xiaomi_app_item')
